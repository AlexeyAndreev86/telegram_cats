import asyncpg
import yaml
from asyncpg import Connection


class DB:
    @staticmethod
    def read_config():
        with open('config.yml') as f:
            setup = yaml.load(f, Loader=yaml.FullLoader)
        return setup

    def __init__(self):
        self.setup = self.read_config()
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(user=self.setup['user'],
                                              password=self.setup['password'],
                                              host=self.setup['host'],
                                              port=self.setup['port'],
                                              database=self.setup['database'])

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
        return result
