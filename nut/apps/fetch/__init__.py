#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.fetch.amazon import Amazon
from apps.fetch.common import get_provider
from apps.fetch.jd import JD
from apps.fetch.kaola import Kaola
from apps.fetch.six_pm import SixPM
from apps.fetch.taobao import TaoBao
from apps.fetch.tmall import Tmall
from apps.fetch.booking import Booking


spider_map = {
    'jd': JD,
    '360buy': JD,
    'taobao': TaoBao,
    '95095': TaoBao,
    'yao': TaoBao,
    'tmall': Tmall,
    'amazon': Amazon,
    'kaola': Kaola,
    'booking': Booking,
    '6pm': SixPM
}


def get_entity_info(entity_url, keys=('title', 'brand', 'price', 'origin_id',
                                      'origin_resource', 'shop_nick', 'link')):
    """
    :param keys: Key need to return.
    :param entity_url: just a url of an entity.
    :returns return a dictionary with keys.
    """

    provider = get_provider(entity_url)
    provider.fetch()

    entity_info = {}
    for key in keys:
        entity_info[key] = provider.get(key, '')
    return entity_info
