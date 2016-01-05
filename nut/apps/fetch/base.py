# -*- coding: utf-8 -*-

from hashlib import md5

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.cache import cache
from django.utils.log import getLogger

from apps.core.tasks import get_html_source
from apps.fetch.common import get_phantom_status, get_origin_source


log = getLogger('django')


class BaseFetcher(object):
    def __init__(self, entity_url):
        self.entity_url = entity_url
        self.origin_source = self.get_origin_source()
        self.html_source = None
        self.expected_element = 'body'

    @property
    def soup(self):
        return BeautifulSoup(self.html_source)

    def fetch(self, timeout=20):
        # html_cache = self.get_html_cache()
        # if html_cache:
        #     return html_cache

        # if get_phantom_status():
        #     response = requests.post(
        #             settings.PHANTOM_SERVER,
        #             data={'url': self.link or self.entity_url,
        #                   'expected_element': self.expected_element,
        #                   'timeout': 10})
        #     self.set_html_cache(response=response)
        #     self.html_source = response.content
        data={'url': self.link or self.entity_url,
              'expected_element': self.expected_element,
              'timeout': 10}
        result = get_html_source.delay(**data)
        self.html_source = result.get()

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

    def get_origin_source(self):
        return get_origin_source(self.entity_url)
