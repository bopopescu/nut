# -*- coding: utf-8 -*-
import codecs
import os, sys

import requests
from django.conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from hashlib import md5
from bs4 import BeautifulSoup
from django.utils.log import getLogger
from django.core.cache import cache

from apps.core.fetch import get_phantom_status


log = getLogger('django')


class Fetcher(object):
    def __init__(self, entity_url, use_phantom=True):
        self.entity_url = entity_url
        self.use_phantom = use_phantom
        self.soup = BeautifulSoup(self.html_source)

    @property
    def header(self):
        origin_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
        }
        return origin_headers

    @property
    def html_source(self):
        return self.fetch_html()

    def fetch_html(self):
        html_cache = self.get_html_cache()
        if html_cache:
            return html_cache

        if self.use_phantom and get_phantom_status():
            response = requests.post(settings.PHANTOM_SERVER_SERVER,
                                     {'url': self.entity_url})
            ufile = codecs.open('/Users/judy/Desktop/phantom.html', 'w',
                                'utf-16')
            ufile.write(response.content.decode('utf8'))
            ufile.close()
            self.set_html_cache(response=response)
            return response.content

    def set_html_cache(self, response):
        if not response:
            return
        key = md5(self.entity_url).hexdigest()
        cache.set(key, {'body': response.content,
                        'header': response.headers})

    def get_html_cache(self):
        key = md5(self.entity_url).hexdigest()

        result = cache.get(key)
        if result:
            return result


if __name__ == "__main__":
    fetcher = Fetcher(
        'https://detail.tmall.com/item.htm?spm=a220o.1000855.0.0.HdNsot&id=45361025253&abbucket=_AB-M193_B8&acm=03194.1003.1.58043&aldid=IpgBaGHA&abtest=_AB-LR193-PR193&scm=1003.1.03194.ITEM_45361025253_58043&pos=2')
    print fetcher.soup
