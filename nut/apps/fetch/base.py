# -*- coding: utf-8 -*-
import requests

from faker import Faker
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.utils.log import getLogger
from hashlib import md5
from selenium.common.exceptions import TimeoutException

from apps.core.tasks import get_html_source
from apps.fetch.common import get_origin_source, clean_images


log = getLogger('django')
faker = Faker()


class BaseFetcher(object):
    def __init__(self, entity_url, use_phantom=False):
        self.entity_url = entity_url
        self.origin_source = self.get_origin_source()
        self.html_source = None
        self.headers = None
        self.expected_element = 'body'
        self.use_phantom = use_phantom

        self._soup = None
        self._images = []
        self._chief_image = None
        self._link = None

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.html_source, from_encoding='utf8')
        return self._soup

    def fetch(self, timeout=20):
        html_source = ''
        headers = ''

        # get html from cache
        # html_cache = self.get_html_cache()
        # if html_cache:
        #     headers = html_cache['header']
        #     html_source = html_cache['body']

        url = self.link or self.entity_url

        if self.use_phantom:
            data = {'url': url,
                    'expected_element': self.expected_element,
                    'timeout': timeout}
            result = get_html_source.delay(**data)

            try:
                html_source = result.get()
            except TimeoutException, e:
                print e.message
                print u'说点啥!!'
        else:
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

    @property
    def chief_image(self):
        if self._chief_image:
            return self._chief_image

        if self._images:
            self._chief_image = self._images[0]
            return self._chief_image

        return []
