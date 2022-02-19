# Получившийся список должен содержать в себе минимум:
#
# 1) Наименование вакансии.
# 2) Предлагаемую зарплату (отдельно минимальную и максимальную; дополнительно - собрать валюту;
#    можно использовать regexp или if'ы).
# 3) Ссылку на саму вакансию.
# 4) Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Сохраните результат в json-файл

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


url = 'https://hh.ru/search/vacancy'
params = {'text': 'python',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)

dom = bs(response.text, 'html.parser')

vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})


# pprint(vacancy_list)

all_vacancy = []
for vacancy in vacancy_list:
    vacancy_data = {}
    name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
    link = vacancy.find('a', {'class': 'bloko-link'})['href']

    vacancy_data['name'] = name
    vacancy_data['link'] = link

    all_vacancy.append(vacancy_data)

pprint(all_vacancy)


