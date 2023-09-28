import configparser
import subprocess

print("Starting...")

settings = configparser.ConfigParser()

if not settings.read('Keys.ini'):
    telegram_key = input('Для начала работы введите Telegram токен:')
    with open('Keys.ini', 'w') as config_file:
        settings.write(config_file)
        config_file.close()


# Запускаем другой файл
subprocess.run(["python", "telegram.py"])