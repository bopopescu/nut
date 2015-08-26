#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import requests
import os
import sys
import settings.production as settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)

CURRENCY_KEY_FORMAT = 'currency.exchange.%s.CNY'


def update_rate(convert_from_list, convert_to='CNY'):
    """ Update exchange rates.

    Request Fixer.io to get the newest exchange rate.
    Rates published by the European Central Bank. The rates are updated daily
    around 3PM CET.
    Base default value is CNY.
    Then set the rate to redis.

    Args: None
    Returns: None
    """
    for convert_from in convert_from_list:
        params = {'base': convert_from,
                  'symbols': convert_to}
        response = requests.get('http://api.fixer.io/latest', params=params)
        rate_info = response.json()

        symbol = 'currency.exchange.%s.%s' % (convert_from, convert_to)
        rate = rate_info['rates'][convert_to]
        r.set(symbol, rate)


def get_rate(convert_from):
    """Get exchange rate.
    Args:
        convert_from: string, the currencies which you want to exchange.

    Returns:
        Decimal.
    """
    redis_key = CURRENCY_KEY_FORMAT % convert_from
    exchange_rate = r.get(redis_key)
    try:
        return float(exchange_rate)
    except ValueError:
        pass


def currency_converting(convert_from, amount):
    """ Currency converting.
    Used Yahoo currency API.

    Args:
        convert_from: A three-letter currency code.
        amount: The amount want to convert. Can be any valid value for decimal
                or integer.
        convert_to: Default CNY. A three-letter currency code.

    Returns:
        A decimal.
    """
    if type(amount) != 'float' or type(amount) != 'int':
        amount = float(amount)
    rate = get_rate(convert_from)
    return round(amount*rate, 2)
