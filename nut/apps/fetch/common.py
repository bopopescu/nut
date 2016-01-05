#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from django.conf import settings
from django.utils.log import getLogger
from urlparse import urlparse, urljoin

from settings import CURRENCY_SYMBOLS


log = getLogger('django')


def get_key(hostname):
    if not hostname:
        return

    if len(hostname) > 2 and hostname.split('.')[-2] == 'com':
        return '.'.join(hostname.split('.')[-3:])
    return '.'.join(hostname.split('.')[-2:])


def get_origin_source(item_url):
    if not item_url:
        return

    hostname = urlparse(item_url).hostname
    if not hostname:
        return

    white_list = ('yao.95095.com',)
    for host_str in white_list:
        if hostname.find(host_str) >= 0:
            return host_str

    if len(hostname) > 2 and hostname.split('.')[-2] == 'com':
        return '.'.join(hostname.split('.')[-3:])
    return '.'.join(hostname.split('.')[-2:])


def get_phantom_status():
    # phantom_health_url = urljoin(settings.PHANTOM_SERVER, '_health')
    # phantom_status = requests.get(phantom_health_url).status_code
    # return phantom_status == 200
    phantom_url = settings.PHANTOM_SERVER
    phantom_status = requests.get(phantom_url).status_code
    return phantom_status == 405


def clean_price_string(prices_string):
    price = None
    if not prices_string:
        return price

    if prices_string.find('-') >= 0:
        price_list = prices_string.split('-')
    else:
        price_list = [prices_string]

    prices = []
    for price_string in price_list:
        price_string = price_string.strip()

        for symbol in CURRENCY_SYMBOLS:
            symbol_index = price_string.find(symbol)
            if symbol_index >= 0:
                price_string = price_string[len(symbol):]
                break

        price_string = price_string.replace(',', '')
        try:
            prices.append(float(price_string))
        except ValueError:
            return

    if len(prices) > 1:
        prices.sort()
    return prices[0]


def get_url_meta(entity_url, keys=('origin_id', 'origin_source', 'link')):
    provider = get_provider(entity_url)
    provider_instance = provider(entity_url)
    values = []
    for key in keys:
        values.append(getattr(provider_instance, key, ''))
    return values


def get_provider(item_url):
    from apps.fetch import spider_map
    host_name = get_origin_source(item_url)
    source_keys = host_name.split('.')
    if source_keys[-2] == 'com':
        source_key = source_keys[-3]
    else:
        source_key = source_keys[-2]

    if source_key and source_key not in spider_map:
        return
    return spider_map[source_key]
