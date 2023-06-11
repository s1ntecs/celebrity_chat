import asyncpg
import asyncio


async def main():
    connection = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='habrpguser',
            database='neural_love',
            password='pgpwd4habr')
    async with connection.transaction():
        query = 'SELECT client_id from client'
        products = await connection.fetch(query)
        for product in products:
            print(product['client_id'])
            create = "INSERT INTO genre VALUES(DEFAULT, 1, $1)"
            await connection.execute(create, product['client_id'])

    await connection.close()


asyncio.run(main())
