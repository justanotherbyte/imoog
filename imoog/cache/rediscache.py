import asyncio

import aioredis

from .basecache import Cache


class RedisCache(Cache):
    async def connect(self, **kwargs):
        connection_uri = kwargs["connection_uri"]
        username = kwargs.get("username")
        password = kwargs.get("password")

        extra_kwargs = {}
        if username and password:
            extra_kwargs["username"] = username
            extra_kwargs["password"] = password

        redis = aioredis.from_url(connection_uri, **extra_kwargs)
        self._connection = redis
        return self._connection
    
    async def get(self, image: str):
        futures = [
            self._connection.get(image),
            self._connection.get(image + "__mime__")
        ]
        r = await asyncio.gather(*futures)

        if None in r:
            return None
            
        return tuple(r)

    async def delete(self, image: str) -> bool:
        futures = [
            self._connection.delete(image),
            self._connection.delete(image + "__mime__")
        ]

        # noinspection PyBroadException
        try:
            await asyncio.gather(*futures)

        except Exception:
            return False

        else:
            return True

    async def set(
        self,
        key: str,
        image: bytes,
        mime: str
    ):
        futures = [
            self._connection.set(key, image),
            self._connection.set(key + "__mime__", mime)
        ]
        await asyncio.gather(*futures)
    
    async def cleanup(self):
        return await self._connection.close()


C_DRIVER = RedisCache
C_DRIVER_TYPE = "REDIS"
