import zlib

class Driver:
    def __init__(self):
        self.pool = None # this connection instance
        # is filled in the connect method.
        self.identifier = None # this is custom per database driver.
        # this attribute will be None until the connect method is called.

    async def connect(self, **kwargs):
        raise NotImplementedError

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
