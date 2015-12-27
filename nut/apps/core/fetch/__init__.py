#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

from urlparse import urlparse, urljoin
from django.conf import settings
from django.utils.log import getLogger

from settings import CURRENCY_SYMBOLS


log = getLogger('django')


def parse_jd_id_from_url(url):
    ids = re.findall(r'\d+', url)
    if len(ids) > 0:
        return ids[0]


def parse_kaola_id_from_url(url):
    ids = re.findall(r'\d+', url)
    if len(ids) > 0:
        return ids[0]


def parse_booking_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split(";"):
        tokens = param.split("=")
        if len(tokens) >= 2 and tokens[0] == "sid":
            return tokens[1]


def get_key(hostname):
    if not hostname:
        return

    if len(hostname) > 2 and hostname.split('.')[-2] == 'com':
        return '.'.join(hostname.split('.')[-3:])
    return '.'.join(hostname.split('.')[-2:])


def get_origin_id_by_url(item_url):
    if not item_url:
        return

    origin_source = get_origin_source_by_url(item_url)
    origin_source_key = get_key(origin_source)
    if origin_source_key in parse_map:
        parse = parse_map[origin_source_key]
        origin_id = parse(item_url)
        return origin_id


def get_origin_source_by_url(item_url):
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
    phantom_health_url = urljoin(settings.PHANTOM_SERVER, '_health')
    phantom_status = requests.get(phantom_health_url).status_code
    return phantom_status == 200


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


parse_map = {
    'jd': parse_jd_id_from_url,
    # 'taobao': parse_taobao_id_from_url,
    # 'tmall': parse_taobao_id_from_url,
    # 'amazon': parse_amazon_id_from_url,
    'kaola': parse_kaola_id_from_url,
    'booking': parse_booking_id_from_url
}
