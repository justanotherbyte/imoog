import zlib
from typing import Any


class Driver:
    def __init__(self, *, conn: Any, identifier: str):
        self._connection = conn # both supported database types
        # will have some sort of supported connection type.
        self.identifier = identifier # an identifier for internal use.
        self.cache_values: dict = {} # some values to store that can be specific
        # to certain drivers. This avoids needing to pass them into the common functions, ruining
        # cross compatability.

    async def insert(self, *args, **kwargs):
        raise NotImplementedError

    async def cleanup(self):
        raise NotImplementedError

    def set_custom_val(self, key: str, value: str):
        self.cache_values[key] = value
        return {key: value}

    def decompress(self, _bytes: bytes) -> bytes:
        decompressed = zlib.decompress(_bytes)
        return decompressed
