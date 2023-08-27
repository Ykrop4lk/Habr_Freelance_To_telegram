import configparser
import telegram
import api

# url = 'https://freelance.habr.com/tasks?categories=development_backend,development_prototyping,development_bots,development_scripts,development_voice_interfaces,development_other,admin_databases,admin_other'
#
# print(api.get_parsed_info(url))

print("Starting...")

settings = configparser.ConfigParser()

if not settings.read('Keys.ini'):
    telegram_key = input('Для начала работы введите Telegram токен:')
    habr_link = input('Для начала работы введите Ссылку на Habr с параметрами поиска:')
    settings['PARAMS'] = {'telegram_key': telegram_key, 'habr_link': habr_link}
    with open('Keys.ini', 'w') as config_file:
        settings.write(config_file)
        config_file.close()

