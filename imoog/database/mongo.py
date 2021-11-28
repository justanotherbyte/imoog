from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from .drivers import Driver # import the base driver impl

if TYPE_CHECKING:
    from motor.motor_asyncio import (
        AsyncIOMotorCollection,
        AsyncIOMotorClient
    )


class MongoDriver(Driver):
    def __init__(self, coll: AsyncIOMotorCollection):
        super().__init__(conn=coll, identifier="mongo")

    async def insert(
        self,
        image: bytes,
        name: str,
        mime: str
    ):
        insert = {
            "_id": name,
            "image": image,
            "mime": mime
        }
        await self._connection.insert_one(insert)
        return 0

    async def fetch(
        self,
        name: str
    ) -> Tuple[bytes, str]:
        query = {"_id": name}
        result = await self._connection.find_one(query)
        image = result["image"]
        mime = result["mime"]
        decompressed = self.decompress(image)
        return (decompressed, mime)

    async def cleanup(self):
        client: AsyncIOMotorClient = self.cache_values["__parent_client__"]
        try:
            await client.close()
        except Exception:
            # disregard any errors here.
            pass

_DRIVER = MongoDriver
_DRIVER_TYPE = "MONGO"