#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

import time


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'
import random
import redis
import requests

from django.conf import settings
from celery.task import task

from apps.core.tasks import BaseTask
from settings import WEIXIN_COOKIE, WEIXIN_KEY
_COOKIE_RE = re.compile(r'(ABTEST=\S+?|SNUID=\S+?|IPLOC=\S+?|SUID=\S+?|black_passportid=\S+?);')


def _get_suv():
    return '='.join(['SUV', str(int(time.time()*1000000) + random.randint(0, 1000))])

r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


@task(base=BaseTask)
def get_cookies(source):
    cookies = r.lrange('cookie:%s' % source, 0, -1)
    if not cookies:
        cookies = set_cookies(source)
    cookie = random.choice(cookies)
    return cookie


@task(base=BaseTask)
def set_cookies(source):
    cookies = []
    for i in xrange(10):

        url = WEIXIN_COOKIE.format(
            q=random.choice('abcdefghijklmnopqrstuvwxyz'))

        # get SNUID
        response = requests.request(method='HEAD', url=url)
        time.sleep(10)
        cookie = process_cookie(response.headers['set-cookie']['Cookie'])
        cookies.append(cookie)

    if cookies:
        r.lpush('cookie:%s' % source, cookies)
    return cookies


@task(base=BaseTask)
def set_key(source):
    url = WEIXIN_KEY.format(id=random.choice('abcdefghijklmnopqrstuvwxyz'))
    response = requests.get(url=url, method='HEAD')
    html = response.content.decode('utf-8')
    key, level, setting = process_key(html)
    r.set('key:%s' % source, (key, level, setting))


def process_cookie(cookie):
    l = _COOKIE_RE.findall(cookie)
    l.append(_get_suv())
    return {'Cookie': '; '.join(l)}


def process_key(html):
    pattern = (
        r'SogouEncrypt.setKv\("(\w+)","(\d)"\)'
        r'.*?'
        r'SogouEncrypt.encryptquery\("(\w+)","(\w+)"\)'
    )
    m = re.findall(pattern, html, re.S)
    key, level, secret, setting = m[0]

    return key, level, setting
