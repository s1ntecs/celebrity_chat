import asyncpg
import asyncio
from SQL_query import (
    CREATE_CHAR_TABLE,
    CREATE_CLIENT_TABLE,
    CREATE_PROMTS_TABLE)


async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='celebrity_dialog',
                                       password='susel')
    statements = [
        CREATE_CHAR_TABLE,
        CREATE_CLIENT_TABLE,
        CREATE_PROMTS_TABLE
        ]
    
    print('sozdaetsya db product....')
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print('db sozdana')
    await connection.close()

asyncio.run(main())
