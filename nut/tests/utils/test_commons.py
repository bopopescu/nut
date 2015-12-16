#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.core.utils.commons import update_rate, get_rate, get_client_ip, \
    get_user_agent


def test_exchange_rate():
    """ It should get latest exchange rate by calling fixer.io API, and store
        in redis.
    """
    symbols = ['USD', 'JPY']
    update_rate(symbols)
    result = get_rate('JPY')
    assert result is not None
    assert type(result) == float


def test_get_client_ip():
    get_client_ip()


def test_get_user_agent():
    get_user_agent()
