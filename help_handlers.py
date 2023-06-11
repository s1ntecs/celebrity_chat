from aiogram import types, Dispatcher
from psql_db.insert_data import (insert_client, get_char_id,
                                 insert_promt, get_character_name,
                                 get_connect)
from openai_bot import get_answer_gpt
from amplitude_new import send_client, get_question
import asyncpg


url = 'https://ai-bot-sintecs.amvera.io/'


async def get_answer(message_text: str,
                     user_id: int,
                     connection_db: asyncpg.Connection):
    char_id = await get_char_id(user_id=user_id,
                                connection_db=connection_db)
    char_name = await get_character_name(char_id,
                                         connection_db)
    answer = await get_answer_gpt(message_text,
                                  char_name)
    return answer, char_id


# Функция-обработчик команды /start
async def send_welcome(message: types.Message):
    """ Создаем клавиатуру с функциями бота. """
    connection = await get_connect()
    await insert_client(message=message, connection_db=connection)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_info = types.web_app_info.WebAppInfo(
        url=url)
    web_app = types.MenuButtonWebApp(
        text="Изменить персонаж", web_app=web_app_info)
    keyboard.add(
        web_app
        )

    # Отправляем сообщение с приветствием и клавиатурой
    await message.answer(
        "Привет! С моей помощью ты можешь поговорить с известной личностью на любые темы:",
        reply_markup=keyboard,
    )


async def handle_messages(message: types.Message):
    if message.text == 'изменить персонаж.':
        await message.answer(
            "Чтобы изменить персонажа, отправьте команду /change_char")
    connection = await get_connect()
    user_id = message.from_user.id
    await get_question(user_id)
    answer, char_id = await get_answer(message.text,
                                       user_id,
                                       connection)
    await insert_promt(message,
                       connection_db=connection,
                       answer=answer,
                       char_id=char_id)
    await message.answer(answer)
    await send_client(user_id)


# Функция-обработчик команды /help
async def send_help(message: types.Message):
    """ Отправляем сообщение с инструкцией по использованию бота. """
    await message.answer(
        "Я могу выполнять следующие команды:\n"
        "/start - начать работу с ботом\n"
        "чтобы изменить персонаж, нажми кнопку Изменить пресонаж\n"
    )


def register_main_handlers(dp: Dispatcher):
    """ Регистрируем обработчики команд. """
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands=["help"])
