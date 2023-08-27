import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import configparser
import os
import tasks_db_operator

# URL сайта, который вы хотите спарсить

base_url = 'https://freelance.habr.com'
keys = configparser.ConfigParser()
keys.read("Keys.ini")
url = keys.get('PARAMS', 'habr_link')
def get_parsed_info(url):

    """
    На вход получает урлу с параметрами для хабра
    На выходе выводит лист со словарями (НЕ ВОЗВРАЩАЕТ)
    
    task_info = {
                'task_id': task_id,
                'task': {
                    'title': title,
                    'price': price,
                    'date': date,
                    'response': response,
                    'desc': description,
                    'tags': tags,
                    'href': full_link
                }
            }
    """

    # Отправка GET-запроса к сайту
    response = requests.get(url)

    if response.status_code == 200:
        list_of_dict = []
        # Инициализация BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Использование регулярного выражения для поиска ссылок
        link_pattern = re.compile(r'<a\s+href="(/tasks/\d+)">')

        # Находим все ссылки
        for match in re.finditer(link_pattern, response.text):
            link = match.group(1)
            full_link = urljoin(base_url, link)  # Полный URL
            if not tasks_db_operator.is_link_in_db(full_link):
                # Отправляем GET-запрос к ссылке и получаем HTML страницы
                task_response = requests.get(full_link)

                # Проверка успешности запроса
                if task_response.status_code == 200:
                    task_soup = BeautifulSoup(task_response.text, 'html.parser')

                    # Извлечение task_id из ссылки
                    task_id = link.split('/')[-1]

                    # Извлечение заголовка
                    title_element = task_soup.find('h2', class_='task__title')
                    title = ' '.join(text.strip() for text in title_element.stripped_strings)

                    # Извлечение цены
                    price_element = task_soup.find('div', class_='task__finance')
                    price = None
                    try:
                        price = price_element.find('span', class_='count').get_text(strip=True) if price_element else ''
                    except:
                        price = price_element.find('span', class_='negotiated_price').get_text(strip=True) if price_element else ''

                    # Извлечение даты
                    date_element = task_soup.find('div', class_='task__meta')
                    date = str(date_element.get_text(strip=True) if date_element else '').replace("\n", "").split("•", 1)[0]


                    # Извлечение количества откликов
                    response_element = task_soup.find('div', class_='task__meta')
                    response = response_element.find('span', class_='count').get_text(strip=True) if response_element else ''

                    # Извлечение тегов
                    tags_element = task_soup.find('div', class_='task__tags')
                    tags_list = []

                    if tags_element:
                        tags_ul = tags_element.find('ul', class_='tags')
                        if tags_ul:
                            tags_li = tags_ul.find_all('li', class_='tags__item')
                            tags_list = [tag.a.get_text(strip=True) for tag in tags_li]

                    tags_string = ' '.join(tags_list)

                    # Извлечение описания
                    description_element = task_soup.find('div', class_='task__description')
                    description = description_element.get_text(strip=True) if description_element else ''

                    # Вывод информации в виде словаря
                    task_info = {
                        'task_id': task_id,
                        'task': {
                            'title': title,
                            'price': price,
                            'date': date,
                            'response': response,
                            'desc': description,
                            'tags': tags_string,
                            'href': full_link
                        }
                    }

                    tasks_db_operator.add_task(task_id, title, price, date, response, description, tags_string, full_link)

                else:
                    raise Exception(f'Ошибка при запросе {full_link}:', task_response.status_code)

    else:
        raise Exception('Ошибка при выполнении запроса:', response.status_code)


if __name__ == '__main__':
    get_parsed_info(url)

