from __future__ import annotations

import importlib
from typing import (
    TYPE_CHECKING,
    Tuple,
    Optional
)

import asyncpg
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from imoog.views import upload_file, deliver_file
from imoog import settings

if TYPE_CHECKING:
    from asyncpg import Pool
    from motor.motor_asyncio import (
        AsyncIOMotorDatabase,
        AsyncIOMotorCollection
    )


routes = [
    Route(
        "/upload",
        upload_file,
        methods=["POST"]
    ),
    Route(
        settings.DELIVER_ENDPOINT + r"{name:str}",
        deliver_file,
        methods=settings.DELIVER_ENDPOINT_METHODS
    )
]

app = Starlette(routes=routes)
app.add_middleware(CORSMiddleware)

app.image_cache = {} # Dict[str, bytes]
app.db_driver = None

def _check_driver() -> Tuple[type, str]:
    _driver_path = settings.DATABASE_DRIVERS["driver"]
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)
    
def update_cache(key: str, value: bytes) -> dict:
    max_size = settings.MAX_CACHE_SIZE
    if len(app.image_cache.keys()) >= max_size:
        return
    
    app.image_cache[key] = value
    return {key: value}

def get_cache(image: str) -> Optional[Tuple[bytes, str]]:
    data = app.image_cache.get(image)
    if data is None:
        return None
    
    mime = data["mime"]
    image = data["image"]
    return (image, mime)
    

app.insert_cache = update_cache
app.get_from_cache = get_cache

@app.on_event("startup")
async def on_startup():
    # connect to databases and ready caches.
    driver_class, _type = _check_driver()
    driver = None
    if _type == "POSTGRES":
        connection_uri = settings.DATABASE_DRIVERS["config"]["connection_uri"]
        min_size = settings.DATABASE_DRIVERS["config"]["min_size"]
        max_size = settings.DATABASE_DRIVERS["config"]["max_size"]
        table = settings.DATABASE_DRIVERS["config"]["table_name"]
        pool: Pool = await asyncpg.create_pool(
            connection_uri,
            min_size=min_size,
            max_size=max_size
        )
        driver = driver_class(pool)
        driver.set_custom_val("__table_name__", table)
    elif _type == "MONGO":
        connection_uri = settings.DATABASE_DRIVERS["config"]["connection_uri"]
        database_name = settings.DATABASE_DRIVERS["config"]["database_name"]
        collection_name = settings.DATABASE_DRIVERS["config"]["collection_name"]
        client = AsyncIOMotorClient(connection_uri)
        _db: AsyncIOMotorDatabase = client[database_name]
        coll: AsyncIOMotorCollection = _db[collection_name]
        driver = driver_class(coll)
        driver.set_custom_val("__parent_client__", client)
    
    app.db_driver = driver


@app.on_event("shutdown")
async def on_shutdown():
    await app.db_driver.cleanup() # all error handling is done within this method.
