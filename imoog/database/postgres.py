from __future__ import annotations

from typing import (
    Tuple,
    Mapping,
    List,
    Any,
    Dict,
    TypeVar,
    Iterable,
    Optional,
    Union
)

import asyncpg

from .drivers import Driver  # import the base driver impl


T = TypeVar("T")


class PostgresDriver(Driver):
    TABLE_NAME: str
    db_pool: asyncpg.Pool

    @staticmethod
    def save_unpack(values: Optional[Iterable[T]], value_count: int = 0) -> Union[Tuple[T], Tuple[None]]:
        if values is None:
            return (None, )*value_count

        if not isinstance(values, list):
            values = tuple(values)

        if len(values) < value_count:
            return values + (None, )*(len(values)-value_count)



    async def connect(self, **kwargs):
        self.identifier = "postgres"

        connection_uri: str = kwargs.get("connection_uri")
        max_size: int = kwargs.get("max_size")
        min_size: int = kwargs.get("min_size")
        table_name: str = kwargs.get("table_name")
        other_kwargs: Dict[str, Any] = kwargs.get("kwargs", {})

        self.TABLE_NAME: str = table_name

        pool = await asyncpg.create_pool(
            connection_uri,
            min_size=min_size,
            max_size=max_size,
            **other_kwargs
        )
        
        self.db_pool = pool
        
        # Creating the table in psql on connect
        # if it doesn't exist.
        async with self.db_pool.acquire() as cursor:
            query = (
                f"CREATE TABLE IF NOT EXISTS {table_name}("
                "name TEXT PRIMARY KEY NOT NULL UNIQUE,"
                "image BYTEA NOT NULL,"
                "mime TEXT NOT NULL"
                ");"
            )
            
            await cursor.execute(query)

        return self.pool

    async def insert(
        self,
        image: bytes,
        name: str,
        mime: str
    ):
        async with self.db_pool.acquire() as cursor:
            query = (
                f"INSERT INTO {self.TABLE_NAME} (name, image, mime) VALUES ($1, $2, $3);"
            )  # this isn't vulnerable to SQL injection, as we have HARD-CODED values
            # controlled by YOU. So if you mess up, this isn't on us.
            await cursor.execute(query, name, image, mime)

        return 0  # why?

    async def fetch(
        self,
        name: str
    ) -> Tuple[bytes, str]:
        async with self.db_pool.acquire() as cursor:
            query = (
                f"SELECT image, mime FROM {self.TABLE_NAME} "
                "WHERE name = $1"
            )
            row: Tuple[bytes, str] = await cursor.fetchrow(query, name)

        image, mime = self.save_unpack(row, 2)
        decompressed = self.decompress(image)

        return decompressed, mime

    async def delete(
        self,
        name: str
    ) -> bool:
        # noinspection PyBroadException
        try:
            async with self.db_pool.acquire() as conn:
                query = (
                    f"DELETE FROM {self.TABLE_NAME} "
                    "WHERE name = $1"
                )
                await conn.execute(query, name)

        except Exception as e:
            return False

        else:
            return True

    async def fetch_all(self) -> List[Mapping[str, Any]]:
        async with self.db_pool.acquire() as conn:
            rows: List[Tuple] = await conn.fetch(f"SELECT * FROM {self.TABLE_NAME}")

        # noinspection PyTypeChecker
        return rows, "name"  # why return this?

    async def cleanup(self):
        return await self.db_pool.close()


DB_DRIVER = PostgresDriver
DB_DRIVER_TYPE = "POSTGRES"
