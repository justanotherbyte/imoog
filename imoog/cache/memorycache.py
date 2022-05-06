from typing import Dict, Union

from .basecache import Cache


class InMemoryCache(Cache):
    _max_size: int

    async def connect(self, **kwargs):
        # to keep it consistent
        # we will indeed have an async function
        # to just register a dict
        self._connection: Dict[str, Union[bytes, str]] = {}
        max_size = kwargs.get("max_cache_size")

        self._max_size = max_size
        return self._connection

    async def get(self, key: str):
        mime = self._connection.get(key + "__mime__")
        image = self._connection.get(key)
        r = (image, mime)

        if None in r:
            return None

        return r

    async def delete(self, key: str) -> bool:
        try:
            self._connection.pop(key)
            self._connection.pop(key + "__mime__")
            # if the first pop fails, the second one will 
            # fail too as its dependent on the first one to exist

        except KeyError:
            return False  # failed

        return True  # success

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


C_DRIVER = InMemoryCache
C_DRIVER_TYPE = "MEMORY"
