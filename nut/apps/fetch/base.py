# -*- coding: utf-8 -*-
import requests

from faker import Faker
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.utils.log import getLogger
from hashlib import md5

from apps.core.tasks import get_html_source
from apps.fetch.common import get_origin_source


log = getLogger('django')
faker = Faker()


class BaseFetcher(object):
    def __init__(self, entity_url):
        self.entity_url = entity_url
        self.origin_source = self.get_origin_source()
        self.html_source = None
        self.headers = None
        self.expected_element = 'body'

    @property
    def soup(self):
        return BeautifulSoup(self.html_source)

    def fetch(self, timeout=20, use_phantom=False):
        html_source = ''
        headers = ''

        # get html from cache
        html_cache = self.get_html_cache()
        if html_cache:
            headers = html_cache['header']
            html_source = html_cache['body']

        url = self.link or self.entity_url

        if use_phantom:
            # get html from phantom
            data = {'url': url,
                    'expected_element': self.expected_element,
                    'timeout': timeout}
            # result = get_html_source.delay(**data)
            result = get_html_source(**data)
            html_source = result.get()
        else:
            # get html from requests
            random_agent = faker.user_agent()
            try:
                response = requests.get(url,
                                        headers={'User-Agent': random_agent})
                headers = response.headers
                html_source = response.content
            except Exception, e:
                log.error(e.message)
                raise

        self.set_html_cache(headers=headers, content=html_source)
        self.html_source = html_source
        self.headers = headers

    def set_html_cache(self, headers, content):
        if not content:
            return
        key = md5(self.entity_url).hexdigest()
        cache.set(key, {'body': content,
                        'header': headers})

    def get_html_cache(self):
        key = md5(self.entity_url).hexdigest()
        result = cache.get(key)
        if result:
            return result

    def get_origin_source(self):
        return get_origin_source(self.entity_url)
