import asyncio
import asyncpg

from data import config

class Database:
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
    
    async def execute(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(sql, *args)

    async def fetch(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(sql, *args)

    async def fetchrow(self, sql, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(sql, *args)
    
    async def disconnect(self):
        await self.pool.close()

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, user_id: int, username: str):
        sql = 'INSERT INTO users (user_id, username) VALUES ($1, $2) ON CONFLICT (user_id) DO NOTHING'
        await self.pool.execute(sql, user_id, username)

    async def select_all_users(self):
        sql = 'SELECT * FROM users'
        return await self.pool.fetch(sql)
    
    async def select_user(self, **kwargs):
        sql = 'SELECT * FROM users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)
    
    async def delete_user(self, user_id):
        sql = 'DELETE FROM users WHERE user_id = $1'
        return await self.pool.execute(sql, user_id)
    
    async def update_user_role(self, user_id, role):
        sql = "UPDATE users SET role = $1 WHERE user_id = $2"
        return await self.pool.execute(sql, role, user_id)

    async def update_username(self, user_id, username):
        sql = "UPDATE users SET username = $1 WHERE user_id = $2"
        return await self.pool.execute(sql, username, user_id)