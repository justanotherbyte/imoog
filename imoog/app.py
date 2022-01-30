from __future__ import annotations

import importlib
from typing import (
    TYPE_CHECKING,
    Tuple
)

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from imoog.views import upload_file, deliver_file, delete_file
from imoog import settings


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
    ),
    Route(
        "/delete",
        delete_file,
        methods=settings.DELETE_ENDPOINT_METHODS
    )
]

app = Starlette(routes=routes)
app.add_middleware(CORSMiddleware, allow_origins = settings.CORS_ALLOWED_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

if settings.ENFORCE_SECURE_SCHEME is True:
    app.add_middleware(HTTPSRedirectMiddleware)

app.image_cache = None
app.db_driver = None

def _check_driver() -> Tuple[type, str]:
    _driver_path = settings.DATABASE_DRIVERS["driver"]
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)

def _check_cache_driver() -> Tuple[type, str]:
    _driver_path = settings.CACHE_DRIVERS["driver"]
    package = importlib.import_module(_driver_path)
    driver = package._DRIVER
    _type = package._DRIVER_TYPE
    return (driver, _type)
    

@app.on_event("startup")
async def on_startup():
    # connect to databases and ready caches.
    driver_class, _ = _check_driver()
    config = settings.DATABASE_DRIVERS["config"]
    driver = driver_class()
    await driver.connect(**config)
    cache_driver_class, _ = _check_cache_driver()
    cache_config = settings.CACHE_DRIVERS["config"]
    cache_driver = cache_driver_class()

    cache_config["max_cache_size"] = settings.MAX_CACHE_SIZE # we pass this into
    # the connect function of the cache driver regardless whether its the
    # memory cache driver or not.
    await cache_driver.connect(**cache_config)

    app.db_driver = driver
    app.image_cache = cache_driver


@app.on_event("shutdown")
async def on_shutdown():
    try:
        await app.db_driver.cleanup()
        await app.cache_driver.cleanup()
    except Exception:
        # disregard any errors that occur
        # within the driver cleanup
        # since this is when our application shuts-down.
        pass
