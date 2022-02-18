import os
import requests
import json
from pprint import pprint
from dotenv import load_dotenv

load_dotenv('../.env')

# task 1 Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую(return) список репозиториев.


def get_repo(token=os.getenv('GIT_API_TOKEN')):

    """The function accepts an api key and returns a list of user repositories"""

    user = str(input('Введи имя пользователя: '))
    url = f'https://api.github.com/users/{user}/repos'
    repos = requests.get(url, auth=(user, token))

    filename = '../repo_data.json'
    with open(filename, "w") as f:
        json.dump(repos.json(), f, indent=4)

    repo_list = []
    for repo in repos.json():
        if not repo['private']:
            repo_list.append(repo['html_url'])

    return repo_list


for num, repository in enumerate(get_repo(), start=1):  # boygaggoo, SenzOne
    print(f'{num}: {repository}')



# task 2 Зарегистрироваться на https://openweathermap.org/api
# написать функцию, которая получает погоду в данный момент для города,
# название которого получается через input. https://openweathermap.org/current


def get_weather(city, url='http://api.openweathermap.org/data/2.5/weather'):

    """Takes a required city argument, and an optional link to openweather.com
       returns a string with city name and temperature """

    token = os.getenv("WEATHER_API_TOKEN", None)
    params = {
        'q': city,
        'appid': token
    }
    response = requests.get(url, params=params)
    json_data = response.json()

    city_name = json_data.get('name')
    temp = round(json_data.get('main').get('temp') - 273.15, 2)

    print(f'В городе {city_name} сейчас {temp}')


get_weather(str(input('Введите название города: ')))  # Moscow, Samara, Sochi

