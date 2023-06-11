import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

# Получаем токен нашего бота из переменной окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
AMPLITUDE_SECRET_KEY = os.getenv("AMPLITUDE_SECRET_KEY")
AMPLITUDE_API_KEY = os.getenv("APLITUDE_API_KEY")
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
