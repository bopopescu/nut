#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import requests
import os
import sys
import settings.dev_judy as settings

__author__ = 'judy'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

r = redis.Redis(host=settings.site_config_host,
                port=settings.site_config_port)


def update_rate():
    """ Update exchange rates.

    Request Fixer.io to get the newest exchange rate.
    Rates published by the European Central Bank. The rates are updated daily
    around 3PM CET.
    Base default value is CNY.
    Then set the rate to redis.

    Args: None
    Returns: None
    """
    convert_to = 'CNY'
    convert_from = 'USD'  # add new symbol with ','

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
    redis_key = 'currency.exchange.%s.CNY' % convert_from
    return float(r.get(redis_key))
