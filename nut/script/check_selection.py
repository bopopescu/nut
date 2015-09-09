#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import settings.dev_judy as settings
import requests
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from apps.core.utils.commons import update_rate
from apps.core.models import Buy_Link, Selection_Entity

# update exchange rate
update_rate(['USD', 'JPY'])


def crawl(buy_link):
    data = {
        'project': 'default',
        'setting': 'DOWNLOAD_DELAY=2',
        'item_id': buy_link.origin_id,
        'update_selection_status': True,
        'spider': ''
    }
    spider = ''
    if buy_link.origin_source == 'taobao.com':
        spider = 'taobao'

    if buy_link.origin_source.find('amazon') >= 0:
        spider = 'amazon'
        data['domain'] = buy_link.origin_source
    data['spider'] = spider

    # res = requests.post('http://10.0.2.48:6800/schedule.json', data=data)
    res = requests.post('http://localhost:6800/schedule.json', data=data)
    return res.json()


now = datetime.datetime.now()
start_time = now - datetime.timedelta(hours=settings.INTERVAL_OF_SELECTION)
end_time = now + datetime.timedelta(hours=settings.INTERVAL_OF_SELECTION)
selections_entity = Selection_Entity.objects.values_list('entity_id').filter(
    pub_time__gte=start_time, pub_time__lte=end_time)
links = Buy_Link.objects.filter(entity_id__in=selections_entity)
for buy_link in links:
    print buy_link.origin_id, crawl(buy_link)
    time.sleep(5)
