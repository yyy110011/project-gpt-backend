import asyncio
import asyncpg

class Database:
    def __init__(self, user, password, database, host, port):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    async def connect(self):
        self.conn = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port
        )

    async def fetch(self, query, *args):
        async with self.conn.acquire() as connection:
            result = await connection.fetch(query, *args)
        return result
    
    async def fetchrow(self, query, *args):
        async with self.conn.acquire() as connection:
            result = await connection.fetchrow(query, *args)
        return result

    async def close(self):
        await self.conn.close()