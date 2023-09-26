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
habr_url = keys.get('PARAMS', 'habr_link')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# @dp.message_handler()
# async def id(message: types.Message):
#     print(message.forward_from_chat.id)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я начну опрашивать БД и отправлять обновления в канал.")
    last_upd = await check_db_changes() # Последний обработанный id
    while True:
        print(1)
        Habr_Scrapper.get_parsed_info(habr_url)
        db_changes = await check_db_changes()
        if last_upd != db_changes:
            last_upd_last = last_upd
            last_upd = db_changes
            number_list = list(range(last_upd_last + 1, last_upd + 1))
            asyncio.create_task(send_task(number_list, message.chat.id))

        await asyncio.sleep(15)


async def send_task(list, chat_id):
    for tasks in list:
        task_id = tasks_db_operator.get_task_id(tasks)
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text="Ссылка", url=tasks_db_operator.get_url_by_task_id(task_id)))
        keyboard.add(InlineKeyboardButton(text="Показать полное описание", callback_data=f"full_description:{task_id}"))

        text = (f"*{tasks_db_operator.get_title_by_task_id(task_id)}*"
                f"\n\n*{tasks_db_operator.get_price_by_task_id(task_id)}*"
                f"\n\n_{tasks_db_operator.get_desc_by_task_id(task_id)[:200]}_"
                f"\n\n_{tasks_db_operator.get_responce_by_task_id(task_id)} Откликов_"
                f"\n\n`{tasks_db_operator.get_tags_by_task_id(task_id)}`"
                f"\n`{tasks_db_operator.get_date_by_task_id(task_id)}`")

        await bot.send_message(text=text, chat_id="-1001958772967", reply_markup=keyboard, parse_mode="markdown")
        await asyncio.sleep(5)

@dp.callback_query_handler(lambda c: c.data == "delete")
async def process_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: "full_description" in c.data)
async def process_callback(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split(":")[1]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Ссылка", url=tasks_db_operator.get_url_by_task_id(task_id)))
    keyboard.add(InlineKeyboardButton(text="Закрыть", callback_data="delete"))

    text = (f"*{tasks_db_operator.get_title_by_task_id(task_id)}*"
            f"\n\n*{tasks_db_operator.get_price_by_task_id(task_id)}*"
            f"\n\n_{tasks_db_operator.get_desc_by_task_id(task_id)}_"
            f"\n\n_{tasks_db_operator.get_responce_by_task_id(task_id)} Откликов_"
            f"\n\n`{tasks_db_operator.get_tags_by_task_id(task_id)}`"
            f"\n`{tasks_db_operator.get_date_by_task_id(task_id)}`")

    await bot.send_message(text=text, chat_id="-1001958772967", reply_markup=keyboard, parse_mode="markdown")


async def check_db_changes():
    conn = sqlite3.connect('database/tasks.db')  # Замените на имя вашей БД
    cursor = conn.cursor()
    last_record = 0
    try:
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")  # Замените на вашу таблицу и поле
        last_record = cursor.fetchone()[0]
    except:
        pass

    return last_record


if __name__ == '__main__':
    # Запуск бота с помощью диспетчера и лонг-поллинга
    executor.start_polling(dp, skip_updates=True)