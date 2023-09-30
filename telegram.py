from aiogram import Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import Database_operators.users_db_operator as db_operator

import configparser

keys = configparser.ConfigParser()
keys.read('Keys.ini')

bot = Bot(token = keys.get('PARAMS', 'telegram_key'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class MyStates(StatesGroup):
    Waiting_For_Email = State()
    Waiting_For_password = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db_operator.add_user(message.from_user.id)
    await message.reply(
        "Привет! Для продолжения работы мне нужны данные твоей учетной записи с Habr.com"
        "\n\nОтправь свою почту:"
    )
    await MyStates.Waiting_For_Email.set()

@dp.message_handler(state=MyStates.Waiting_For_Email)
async def waiting_for_email(message: types.Message, state: FSMContext):
    db_operator.add_email(message.from_user.id, message.text)
    await state.finish()
    await message.delete()
    await bot.send_message(text="Почта успешно сохранена"
                                "\n\n Теперь отправь свой пароль:", chat_id=message.chat.id)
    await MyStates.Waiting_For_password.set()

@dp.message_handler(state=MyStates.Waiting_For_password)
async def waiting_for_password(message: types.Message, state: FSMContext):
    db_operator.add_password(message.from_user.id, message.text)
    await state.finish()
    await message.delete()
    await bot.send_message(text="Пароль успешно сохранен", chat_id=message.chat.id)


if __name__ == '__main__':
    # Запуск бота с помощью диспетчера и лонг-поллинга
    executor.start_polling(dp, skip_updates=True)