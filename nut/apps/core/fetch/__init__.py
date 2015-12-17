#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from urlparse import urlparse
from urllib import unquote_plus
from django.utils.log import getLogger
from apps.core.fetch.jd import JD
from apps.core.fetch.tmall import Tmall
from apps.core.fetch.kaola import Kaola
from apps.core.fetch.six_pm import SixPM
from apps.core.fetch.taobao import TaoBao
from apps.core.fetch.amazon import Amazon
from apps.core.fetch.booking import Booking


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


def get_key(item_url):
    assert item_url is not None
    origin_source_key = urlparse(item_url).hostname.split('.')[1]
    return origin_source_key


def get_origin_id_by_url(item_url):
    origin_source_key = get_key(item_url)
    if origin_source_key in parse_map:
        parse = parse_map[origin_source_key]
        origin_id = parse(item_url)
        return origin_id


def get_origin_source_by_url(item_url):
    hostname = urlparse(item_url).hostname
    print '>>>>>> host: ', hostname
    if not hostname:
        return
    if re.search(r"\b(taobao|tmall|95095)\.(com|hk)$", hostname) is not None:
        return 'taobao.com'
    if re.search(r"\b(amazon)\.w+$", hostname) is not None:
        return 'amazon.com'
    if hostname.endswith('jd.com'):
        return 'jd.com'
    else:
        return hostname


parse_map = {
    'jd': parse_jd_id_from_url,
    'taobao': parse_taobao_id_from_url,
    'tmall': parse_taobao_id_from_url,
    'amazon': parse_amazon_id_from_url,
    'kaola': parse_kaola_id_from_url,
    'booking': parse_booking_id_from_url
}

spider_map = {
    'jd': JD,
    '360buy': JD,
    'taobao': TaoBao,
    '95095': TaoBao,
    'tmall': Tmall,
    'amazon': Amazon,
    'kaola': Kaola,
    'booking': Booking,
    '6pm': SixPM
}
