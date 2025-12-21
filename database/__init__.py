import asyncpg
from data import config
from .create_table import *
from .users_manager import UsersManager
from .requests_manager import RequestsManager

class Database(CreateTable, UsersManager, RequestsManager):
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.PG_USER,
            password=config.PG_PASSWORD,
            database=config.PG_DATABASE,
            host=config.PG_HOST,
            port=config.PG_PORT
        )
    
    async def disconnect(self):
        await self.pool.close()
    
    async def execute(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(sql, *args)

    async def fetch(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql, *args)

    async def fetchrow(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(sql, *args)
    
    async def fetchval(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(sql, *args)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())