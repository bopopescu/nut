#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.fetch.entity.amazon import Amazon
from apps.fetch.entity.booking import Booking
from apps.fetch.entity.jd import JD
from apps.fetch.entity.kaola import Kaola
from apps.fetch.entity.six_pm import SixPM
from apps.fetch.entity.taobao import TaoBao
from apps.fetch.entity.tmall import Tmall
from apps.fetch.common import get_provider


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
    provider_instance = provider(entity_url)
    provider_instance.fetch()

    entity_info = {}
    for key in keys:
        entity_info[key] = getattr(provider_instance, key, '')
    return entity_info
