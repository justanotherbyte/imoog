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
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
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
app.add_middleware(CORSMiddleware, allow_origins = settings.CORS_ALLOWED_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

if settings.ENFORCE_SECURE_SCHEME is True:
    app.add_middleware(HTTPSRedirectMiddleware)

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
    if len(app.image_cache.keys()) >= float(max_size):
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
    driver_class, _ = _check_driver()
    config = settings.DATABASE_DRIVERS["config"]
    driver = driver_class()
    await driver.connect(**config)
    
    app.db_driver = driver


@app.on_event("shutdown")
async def on_shutdown():
    try:
        await app.db_driver.cleanup()
    except Exception:
        # disregard any errors that occur
        # within the driver cleanup
        # since this is when our application shuts-down.
        pass
