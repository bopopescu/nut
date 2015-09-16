#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
import time
import requests


<<<<<<< HEAD

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from apps.core.utils.commons import update_rate
from apps.core.models import Buy_Link, Entity

=======
>>>>>>> 1c861993ecc066feb5a908dd3c1a274592db055a
# update exchange rate
update_rate(['USD', 'JPY'])


def crawl(spider, **parameters):
    data = {
        'project': 'default',
        'setting': 'DOWNLOAD_DELAY=2',
    }
    data.update(parameters)
    res = requests.post('http://10.0.2.48:6800/schedule.json', data=data)
    return res.json()


# Taobao
links = Buy_Link.objects.filter(origin_source='taobao.com',
                                entity__status__gt=Entity.new).\
    exclude(status=Buy_Link.remove).order_by('-id')
# print links.count()
for row in links:
    print row.origin_id, crawl(item_id=row.origin_id,
                               spider='taobao')
    time.sleep(5)


# Amazon
# links = Buy_Link.objects.filter(origin_source__in=('www.amazon.com',
#                                                    'www.amazon.cn'),
#                                 entity__status__gt=Entity.new) \
#     .exclude(status=Buy_Link.remove) \
#     .order_by('-id')
#
# for row in links:
#     print row.origin_id, crawl(item_id=row.origin_id,
#                                domain=row.origin_source,
#                                spider='amazon')
#     time.sleep(5)

__author__ = 'edison'
