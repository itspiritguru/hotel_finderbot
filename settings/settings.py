"""
Файл содержащий базовые конфигурации бота и API (Токен, API-ключ, заголовок, параметры и url-адреса)
"""

import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()

TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')


HEADERS = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': API_KEY
}


URL_SEARCH = 'https://hotels4.p.rapidapi.com/locations/v3/search'
URL_PROPERTY_LIST = 'https://hotels4.p.rapidapi.com/properties/v2/list'
URL_PHOTO = 'https://hotels4.p.rapidapi.com/properties/v2/get-summary'
URL_DETAILHOTEL = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
URL_HOTEL = 'https://www.hotels.com/ho{}'


EXCHANGE_DOLLAR = 72
EXCHANGE_EURO = 78

QUERY_SEARCH = {
    'q': 'new_york',
    'locale': 'en_US',
    'currency': 'USD',
    'langid': '1033',
    'siteid': '300000001'
}
QUERY_PROPERTY_LIST = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {
        "regionId": "6054439"
    },
    "checkInDate": {
        "day": 12,
        "month": 1,
        "year": 2023
    },
    "checkOutDate": {
        "day": 15,
        "month": 1,
        "year": 2023
    },
    "rooms": [
        {
            "adults": 1
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 25,
    "sort": "PRICE_LOW_TO_HIGH",
}
QUERY_custom = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {
        "regionId": "6054439"
    },
    "checkInDate": {
        "day": 12,
        "month": 1,
        "year": 2023
    },
    "checkOutDate": {
        "day": 15,
        "month": 1,
        "year": 2023
    },
    "rooms": [
        {
            "adults": 1
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 25,
    "sort": "DISTANCE",
    "filters": {
        "price": {
            "max": 300,
            "min": 50
        }
    }
}
QUERY_PHOTO = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612"
}
QUERY_HOTEL = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "propertyId": "9209612"
}
