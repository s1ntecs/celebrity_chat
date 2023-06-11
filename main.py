import asyncpg
from aiogram.utils import executor
from create_bot import dp
from help_handlers import register_main_handlers, handle_messages
from psql_db.insert_data import change_character, get_connect

if __name__ == "__main__":
    register_main_handlers(dp=dp)

    @dp.message_handler(content_types="web_app_data")
    async def get_data(webAppMes):
        connection = await get_connect()
        await change_character(message=webAppMes,
                               connection_db=connection)
    dp.register_message_handler(handle_messages)
    executor.start_polling(dp, skip_updates=True)
