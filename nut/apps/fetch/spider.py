#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.fetch.common import get_provider


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
