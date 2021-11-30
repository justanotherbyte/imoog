from typing import Dict

from .basecache import Cache


class InMemoryCache(Cache):
    async def connect(self, **kwargs):
        # to keep it consistent
        # we will indeed have an async function
        # to just register a dict
        self._connection: Dict[str, bytes] = {}
        max_size = kwargs["max_cache_size"]

        self._max_size = max_size
        return self._connection

    async def get(self, key: str):
        mime = self._connection.get(key + "__mime__")
        image = self._connection.get(key)
        R = (image, mime)
        if None in R:
            return None
        
        return R

    async def set(
        self,
        key: str,
        image: bytes,
        mime: str
    ):
        self._connection[key] = image
        self._connection[key + "__mime__"] = mime
    
    async def cleanup(self):
        # believe it or not
        # there is a cleanup operation for a dictionary
        # we'll free the memory by clearing the dictionary
        self._connection.clear()

_DRIVER = InMemoryCache
_DRIVER_TYPE = "MEMORY"