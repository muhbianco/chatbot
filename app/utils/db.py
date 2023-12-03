import os

# import mysql.connector
from asyncmy import connect
from asyncmy.cursors import DictCursor
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class DB:
    config = {
        "host": os.environ["DATABASE_HOST"],
        "user": os.environ["DATABASE_USER"],
        "password": os.environ["DATABASE_PASS"],
        "database": os.environ["DATABASE_NAME"],
    }

    async def query(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, args)
                await conn.commit()

    async def insert(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, args)
                await conn.commit()
                return cursor.lastrowid

    async def insertmany(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(sql, args)
                await conn.commit()
                return cursor.rowcount

    async def update(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, args)
                rowcount = cursor.rowcount
                await conn.commit()
                return rowcount

    async def fetch(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(sql, args)
                rows = await cursor.fetchall() if cursor.with_rows else []
                return rows

    async def fetchone(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(sql, args)
                row = await cursor.fetchone()
                return row

    async def delete(self, sql, args: tuple = ()):
        async with connect(**self.config) as conn:
            async with conn.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(sql, args)
                rowcount = cursor.rowcount
                await conn.commit()
                return rowcount