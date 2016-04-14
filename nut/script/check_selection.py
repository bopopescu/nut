#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

import requests
import datetime


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
    }
    spider = ''
    if buy_link.origin_source == 'taobao.com':
        spider = 'taobao'

    if buy_link.origin_source.find('amazon') >= 0:
        spider = 'amazon'
        data['domain'] = buy_link.origin_source
    data['spider'] = spider

    res = requests.post('http://10.0.2.49:6800/schedule.json', data=data)
    return res.json()

now = datetime.datetime.now()
start_time = now - datetime.timedelta(hours=settings.INTERVAL_OF_SELECTION)
end_time = now + datetime.timedelta(hours=settings.INTERVAL_OF_SELECTION)
selections_entity = Selection_Entity.objects.values_list('entity_id').filter(
    pub_time__gte=start_time, pub_time__lte=end_time)

links = Buy_Link.objects.filter(entity_id__in=selections_entity)

while True:

    for index, buy_link in enumerate(links):
        print(index, crawl(buy_link))
        time.sleep(5)
    else:
        links = Buy_Link.objects.filter(entity_id__in=selections_entity)
        time.sleep(60)



# @app.task(name='check_selection')
# def check_selection():
#     global LINKS
#     if not LINKS:
#         LINKS = list(Buy_Link.objects.filter(entity_id__in=selections_entity))
#     crawl(LINKS.pop())
#     print(datetime.datetime.now())
#     print(len(LINKS))
#     print '-'*80






