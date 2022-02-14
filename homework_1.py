import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv('./.env')


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


get_weather(str(input('Введи название города: ')))  # Moscow, Samara, Sochi

