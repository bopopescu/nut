#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

from urlparse import urlparse
from django.conf import settings
from django.utils.log import getLogger


log = getLogger('django')


def parse_amazon_id_from_url(url):
    parts = url.split('/')
    if u'product' in parts:
        return parts[parts.index(u'product') + 1]
    if u'dp' in parts:
        return parts[parts.index(u'product') + 1]


def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
            # url = unquote_plus(url)
            # params = url.split("?")[1]
            # for param in params.split("&"):
            #     tokens = param.split("=")
            #     if len(tokens) >= 2 and (tokens[0] == "id"
            #                              or tokens[0] == "item_id"
            #                              or tokens[1] == 'itemid'):
            #         return tokens[-1]


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
    phantom_url = settings.PHANTOM_SERVER_SERVER
    phantom_status = requests.get(phantom_url).status_code
    return phantom_status == 405


parse_map = {
    'jd': parse_jd_id_from_url,
    'taobao': parse_taobao_id_from_url,
    'tmall': parse_taobao_id_from_url,
    'amazon': parse_amazon_id_from_url,
    'kaola': parse_kaola_id_from_url,
    'booking': parse_booking_id_from_url
}
