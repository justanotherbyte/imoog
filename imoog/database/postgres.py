from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from .drivers import Driver # import the base driver impl

if TYPE_CHECKING:
    from asyncpg import Pool


class PostgresDriver(Driver):
    def __init__(self, pool: Pool):
        super().__init__(conn=pool, identifier="psql")

    async def insert(
        self,
        image: bytes,
        name: str,
        mime: str
    ):
        table_name = self.cache_values["__table_name__"]
        async with self._connection.acquire() as conn:
            query = (
                f"INSERT INTO {table_name} (name, image, mime) VALUES ($1, $2, $3)"
            ) # this isn't vulnerable to SQL injection, as we have HARD-CODED values
            # controlled by YOU. So if you mess up, this isn't on us.
            await conn.execute(query, name, image, mime)

        return 0

    async def fetch(
        self,
        name: str
    ) -> Tuple[bytes, str]:
        table_name = self.cache_values["__table_name__"]
        async with self._connection.acquire() as conn:
            query = (
                f"SELECT image FROM {table_name} "
                "WHERE name = $1"
            )
            row = await conn.fetchrow(query, name)
    
        image = row["image"]
        mime = row["mime"]
        decompressed = self.decompress(image)
        return (decompressed, mime)
        
    async def cleanup(self):
        try:
            await self._connection.close()
        except Exception:
            # disregard any errors that occur here.
            pass

_DRIVER = PostgresDriver
_DRIVER_TYPE = "POSTGRES"