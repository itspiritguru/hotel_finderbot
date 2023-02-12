import json
from typing import List, Dict

import requests
import string

from requests import Response
from telebot.types import Message, CallbackQuery
from database.models import user
from loader import logger, exception_request_handler
from settings import constants
from settings.settings import QUERY_SEARCH, URL_SEARCH, HEADERS, QUERY_PROPERTY_LIST, URL_PROPERTY_LIST, QUERY_PHOTO, \
    URL_PHOTO, QUERY_custom, QUERY_HOTEL, URL_DETAILHOTEL


@exception_request_handler
def request_search(message: Message) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/locations/v3/search'
    Проверяет введённые пользователем символы на ASCII кодировку, если так, то ищет с параметром locale en_US,
    в противном случае ищет с парметром locale ru_RU. Возвращает Response, содержащий в себе список городов.

    :param message: Message
    :return: Response
    """
    logger.info(str(message.from_user.id))
    for sym in message.text:
        if sym not in string.printable:
            QUERY_SEARCH['locale'] = 'ru_RU'
            break
    QUERY_SEARCH['currency'] = user.user.currency
    QUERY_SEARCH['q'] = message.text
    user.edit('locale', QUERY_SEARCH['locale'])
    response = requests.request('GET', URL_SEARCH, headers=HEADERS, params=QUERY_SEARCH, timeout=15)
    return response


@exception_request_handler
def request_property_list(call: CallbackQuery) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/list'
    Предназначена для команд lowprice и highprice. В зависимости от введенной команды сортирует ответ
    по возврастанию цены, или же по убыванию. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))
    if user.user.command == constants.HIGHPRICE[1:]:
        QUERY_PROPERTY_LIST['sort'] = '-PRICE_LOW_TO_HIGH'
    QUERY_PROPERTY_LIST['destination']['regionId'] = user.user.city_id
    QUERY_PROPERTY_LIST['checkInDate']['year'] = int(user.user.date_in.split('-')[0])
    QUERY_PROPERTY_LIST['checkInDate']['month'] = int(user.user.date_in.split('-')[1])
    QUERY_PROPERTY_LIST['checkInDate']['day'] = int(user.user.date_in.split('-')[2])
    QUERY_PROPERTY_LIST['checkOutDate']['year'] = int(user.user.date_out.split('-')[0])
    QUERY_PROPERTY_LIST['checkOutDate']['month'] = int(user.user.date_out.split('-')[1])
    QUERY_PROPERTY_LIST['checkOutDate']['day'] = int(user.user.date_out.split('-')[2])
    QUERY_PROPERTY_LIST['currency'] = user.user.currency
    QUERY_PROPERTY_LIST['locale'] = user.user.locale
    response = requests.request('POST', URL_PROPERTY_LIST, headers=HEADERS, json=QUERY_PROPERTY_LIST, timeout=15)
    return response


@exception_request_handler
def request_custom(call: CallbackQuery) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/list'. Предназначена для
    команды custom. Исключительность данной функции под функционал одной команды заключается в широкой
    установке параметров для поиска. Возвращает Response, содержащий в себе список отелей в выбранном городе.

    :param call: CallbackQuery
    :return: Response
    """
    logger.info(str(call.from_user.id))

    QUERY_custom['destination']['regionId'] = user.user.city_id
    QUERY_custom['checkInDate']['year'] = int(user.user.date_in.split('-')[0])
    QUERY_custom['checkInDate']['month'] = int(user.user.date_in.split('-')[1])
    QUERY_custom['checkInDate']['day'] = int(user.user.date_in.split('-')[2])
    QUERY_custom['checkOutDate']['year'] = int(user.user.date_out.split('-')[0])
    QUERY_custom['checkOutDate']['month'] = int(user.user.date_out.split('-')[1])
    QUERY_custom['checkOutDate']['day'] = int(user.user.date_out.split('-')[2])
    QUERY_custom['currency'] = user.user.currency
    QUERY_custom['locale'] = user.user.locale
    response = requests.request('POST', URL_PROPERTY_LIST, headers=HEADERS, json=QUERY_custom, timeout=15)
    return response


@exception_request_handler
def request_get_photo(call: CallbackQuery, hotel_id: int) -> Response:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/get-summary'.
    Вызывается при необходимости вывода фотографий к отелям. Возвращает Response, содержащий в себе список url
    фотографий отелей.

    :param call: CallbackQuery
    :param hotel_id: int
    :return: Response
    """
    logger.info(str(call.from_user.id))
    QUERY_PHOTO['propertyId'] = hotel_id
    response = requests.request('POST', URL_PHOTO, headers=HEADERS, json=QUERY_PHOTO, timeout=15)
    return response


@exception_request_handler
def request_hotel_detail(call: CallbackQuery, hotel_id: int) -> Dict:
    """
    Функция - делающая запрос на API по адресу: 'https://hotels4.p.rapidapi.com/properties/v2/get-summary'.
    Вызывается при необходимости вывода фотографий к отелям. Возвращает Response, содержащий в себе список url
    фотографий отелей.

    :param call: CallbackQuery
    :param hotel_id: int
    :return: Dict
    """
    logger.info(str(call.from_user.id))
    QUERY_HOTEL['propertyId'] = hotel_id
    response = requests.request('POST', URL_DETAILHOTEL, headers=HEADERS, json=QUERY_HOTEL, timeout=15)
    get_res = json.loads(response.text)
    return get_res['data']['propertyInfo']['summary']


