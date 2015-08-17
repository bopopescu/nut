#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'judy'

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from apps.core.models import Buy_Link, Entity
import requests
import time


def crawl(item_id, domain):
    data = {
        'project': 'default',
        'spider': 'amazon',
        'setting': 'DOWNLOAD_DELAY=2',
        'item_id': item_id,
        'domain': domain
    }
    res = requests.post('http://10.0.2.48:6800/schedule.json', data=data)
    return res.json()

links = Buy_Link.objects.filter(origin_source__in=('www.amazon.com',
                                                   'www.amazon.cn'),
                                entity__status__gt=Entity.new).exclude(
    status=Buy_Link.remove).order_by('-id')


for row in links:
    print row.origin_id, crawl(item_id=row.origin_id, domain=row.origin_source)
    time.sleep(5)
