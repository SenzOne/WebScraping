# Получившийся список должен содержать в себе минимум:
#
# 1) Наименование вакансии.
# 2) Предлагаемую зарплату (отдельно минимальную и максимальную; дополнительно - собрать валюту;
#    можно использовать regexp или if'ы).
# 3) Ссылку на саму вакансию.
# 4) Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Сохраните результат в json-файл

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import pandas as pd
from time import sleep


@dataclass
class Vacancy:
    name = str
    domain = str
    salary = str
    min_salary = int
    max_salary = int
    currency = str
    site = str


    def get_salary_hh(self, salary_str):
        # self.salary = salary_str.replace('\u202f', '')
        self.currency = salary_str.split()[-1]
        if salary_str.find('–') != -1:
            self.min_salary = int(salary_str.replace('\u202f', '').split()[0])
            self.max_salary = int(salary_str.replace('\u202f', '').split()[2])
        elif salary_str.find('от') != -1:
            self.min_salary = int(salary_str.replace('\u202f', '').split()[1])
            self.max_salary = None
        elif salary_str.find('до') != -1:
            self.min_salary = None
            self.max_salary = int(salary_str.replace('\u202f', '').split()[1])
        else:
            self.min_salary = None


class VacancyList:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/97.0.4692.71 '
                      'Safari/537.36'}

    def __init__(self, vacancy_text, page=2):
        self.all_vacancy = []
        self.vacancy_text = vacancy_text
        self.page_count = page
        self.add_hh()

    def add_vacancy(self, vacancy):
        self.all_vacancy.append(vacancy)

    def add_hh(self):
        domain = 'https://hh.ru'
        url = '/search/vacancy'
        params_dict = {'clusters': 'true',
                       'area': 1,
                       'enable_snippets': 'true',
                       'st': 'searchVacancy',
                       'text': self.vacancy_text,
                       'page': 0}

        for page_count in range(0, self.page_count):
            params_dict['page'] = page_count
            response = requests.get(domain + url, params=params_dict, headers=self.headers)
            dom = BeautifulSoup(response.text, 'html.parser')

            card_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

            for card in card_list:
                vacancy = Vacancy()
                vacancy.site = 'hh.ru'
                vacancy.name = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
                vacancy.domain = domain
                vacancy.link = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

                try:
                    salary = card.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    vacancy.get_salary_hh(salary)

                except AttributeError:
                    vacancy.salary = None
                    vacancy.min_salary = None
                    vacancy.max_salary = None
                    vacancy.currency = None

                self.all_vacancy.append(vacancy)
            print(f'Обработка страницы {page_count + 1}')
            sleep(1)


final_list = VacancyList(vacancy_text='Data scientist', page=3)

vac_data = []
for vacancy in final_list.all_vacancy:
    vacancy_dict = {'name': vacancy.name,
                    # 'site': vacancy.site,
                    'link': vacancy.link,
                    'max_salary': vacancy.max_salary,
                    'min_salary': vacancy.min_salary,
                    'currency': vacancy.currency
                    }

    vac_data.append(vacancy_dict)

# with open('vacancy_data.txt', 'w') as f:
#     for i in vac_data:
#         f.write(str(i) + '\n')

with open('vacancy_data.txt', 'r') as f:
    print(f.read())

