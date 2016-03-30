#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from spider import settings

r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


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


def get_rate(convert_from):
    """Get exchange rate.
    Args:
        convert_from: string, the currencies which you want to exchange.

    Returns:
        Decimal.
    """
    redis_key = 'currency.exchange.%s.CNY' % convert_from
    return float(r.get(redis_key))
