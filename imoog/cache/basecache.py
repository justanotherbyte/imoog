class Cache:
    # a base cache handler
    def __init__(self):
        self._connection = None # this is similar
        # to the database handlers, except this can also just
        # be a regular dictionary

    async def connect(self, *args, **kwargs):
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def set(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs) -> int:
        raise NotImplementedError
    
    async def cleanup(self):
        raise NotImplementedError
