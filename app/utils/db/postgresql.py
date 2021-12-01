import logging

from asyncpg import create_pool
from asyncpg.pool import Pool

from app.utils.config_reader import DB
from app.utils.db.base import DatabaseBase


class Database(DatabaseBase):
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls, db_config: DB):
        logging.info("Connecting to DB...")
        pool = await create_pool(**db_config.__dict__)
        return cls(pool)

    async def add_user(self, **kwargs):
        sql, values = self._insert_args(table="users", column_values=kwargs)
        await self.pool.execute(sql, *values)

    async def get_user_lang(self, user_id: int):
        sql, values = self._select_where_args("users", ["lang"], {"telegram_id": user_id})
        return await self.pool.execute(sql, *values)

    async def set_user_lang(self, user_id: int, lang: str):
        sql = """UPDATE users SET lang = $1 WHERE telegram_id = $2"""
        values = (lang, user_id)
        await self.pool.execute(sql, *values)
