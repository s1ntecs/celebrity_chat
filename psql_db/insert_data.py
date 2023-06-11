import asyncpg
from aiogram import types
from amplitude import register_user, user_changed_char


async def get_connect():
    """ Создаем клавиатуру с функциями бота. """
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='celebrity_dialog',
                                       password='susel')
    return connection


async def user_is_exist(message: types.Message,
                        connection_db: asyncpg.Connection):
    select_query = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = $1)"
    result = await connection_db.fetchval(select_query, message.from_user.id)
    return result


async def insert_client(message: types.Message,
                        connection_db: asyncpg.Connection):
    if await user_is_exist(message, connection_db):
        return
    insert_query = """INSERT INTO users (
        user_id, username, name, surname, time)
        VALUES ($1, $2, $3, $4, $5)"""
    values = (message.from_user.id,
              message.from_user.username,
              message.from_user.first_name,
              message.from_user.last_name,
              message.date)

    await connection_db.execute(insert_query, *values)
    await register_user(message.from_user.id)


async def get_character_name(char_id: int,
                             connection_db: asyncpg.Connection) -> str:
    char_query = "SELECT name FROM characters WHERE char_id = $1"
    char_name = await connection_db.fetchval(char_query, char_id)
    return char_name


async def get_char_id(user_id: int,
                      connection_db: asyncpg.Connection) -> int:
    char_query = "SELECT current_char_id FROM users WHERE user_id = $1"
    char_id = await connection_db.fetchval(char_query, user_id)
    return char_id


async def get_welcome_msg(char_id: int,
                          connection_db: asyncpg.Connection) -> int:
    char_query = "SELECT welcome_msg FROM characters WHERE char_id = $1"
    welcome_msg = await connection_db.fetchval(char_query, char_id)
    return welcome_msg


async def insert_promt(message: types.Message,
                       connection_db: asyncpg.Connection,
                       char_id: int,
                       answer: str):
    insert_query = """
    INSERT INTO promts (user_id, character_id, question, answer)
    VALUES ($1, $2, $3, $4)
    RETURNING promt_id
    """

    values = (message.from_user.id,
              char_id,
              message.text,
              answer)

    await connection_db.execute(insert_query, *values)
    return char_id


async def change_character(message: types.Message,
                           connection_db: asyncpg.Connection):
    select_query = "SELECT current_char_id FROM users WHERE user_id = $1"
    user_id = message.from_user.id
    result = await connection_db.fetchrow(select_query, user_id)

    if result is not None:
        current_char_id = result['current_char_id']
        new_char_id = int(message.web_app_data.data)
        msg = await get_welcome_msg(new_char_id, connection_db)
        if current_char_id != new_char_id:
            update_query = """
            UPDATE users SET current_char_id = $1 WHERE user_id = $2
            """
            await connection_db.execute(update_query, new_char_id, user_id)
            # Отправим в Amplitude об изменении персонажа
            await user_changed_char(user_id)
            msg = await get_welcome_msg(new_char_id, connection_db)
            await message.answer(msg)
        else:
            await message.answer(msg)
    else:
        await message.answer("User not found.")
