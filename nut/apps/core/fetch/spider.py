#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apps.core.fetch import get_origin_source
from apps.core.fetch.jd import JD
from apps.core.fetch.tmall import Tmall
from apps.core.fetch.kaola import Kaola
from apps.core.fetch.six_pm import SixPM
from apps.core.fetch.taobao import TaoBao
from apps.core.fetch.amazon import Amazon
from apps.core.fetch.booking import Booking


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
    print entity_info


def get_provider(item_url):
    host_name = get_origin_source(item_url)
    source_keys = host_name.split('.')
    if source_keys[-2] == 'com':
        source_key = source_keys[-3]
    else:
        source_key = source_keys[-2]

    if source_key and source_key not in spider_map:
        return
    return spider_map[source_key]


################################################################################
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
