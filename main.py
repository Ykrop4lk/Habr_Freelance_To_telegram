import configparser
import subprocess
import sqlite3

conn = sqlite3.connect("database/tasks.db")
cur = conn.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task_id TEXT,
            title TEXT,
            price TEXT,
            "date" TEXT,
            responce TEXT,
            description TEXT,
            tags TEXT,
            href TEXT
        )
    ''')

conn.commit()
conn.close()

print("Starting...")

settings = configparser.ConfigParser()

if not settings.read('Keys.ini'):
    telegram_key = input('Для начала работы введите Telegram токен:')
    habr_link = input('Для начала работы введите Ссылку на Habr с параметрами поиска:')
    settings['PARAMS'] = {'telegram_key': telegram_key, 'habr_link': habr_link}
    with open('Keys.ini', 'w') as config_file:
        settings.write(config_file)
        config_file.close()


# Запускаем другой файл
subprocess.run(["python", "telegram.py"])