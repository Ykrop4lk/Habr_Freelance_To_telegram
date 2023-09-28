from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from aiogram import types
import configparser
import sqlite3
import Habr_Scrapper
import tasks_db_operator

keys = configparser.ConfigParser()
keys.read('Keys.ini')

bot = Bot(token = keys.get('PARAMS', 'telegram_key'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я начну опрашивать БД и отправлять обновления в канал.")



if __name__ == '__main__':
    # Запуск бота с помощью диспетчера и лонг-поллинга
    executor.start_polling(dp, skip_updates=True)