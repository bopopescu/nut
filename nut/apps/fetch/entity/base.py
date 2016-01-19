# -*- coding: utf-8 -*-
from hashlib import md5

import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.utils.log import getLogger
from faker import Faker
from selenium.common.exceptions import TimeoutException, WebDriverException

from apps.core.tasks import get_html_source
from apps.fetch.common import get_origin_source, process_cookie


log = getLogger('django')
faker = Faker()


class BaseFetcher(object):
    def __init__(self, entity_url, use_phantom=False):
        self.entity_url = entity_url
        self.html_source = None
        self.expected_element = 'body'
        self.use_phantom = use_phantom
        self.timeout = None
        self._soup = None
        self._images = []
        self._chief_image = None
        self._link = None
        self._headers = None
        self._cookie = None
        self._referer = ''
        self.origin_source = self.get_origin_source()

    @property
    def headers(self):
        if not self._headers:
            headers = {'UserAgent': faker.user_agent(),
                       'Referer': self._referer,
                       'Cookie': self.cookie,
            }
            self._headers = headers
        return self._headers

    @property
    def cookie(self):
        return self._cookie

    def fetch(self):
        html_source = ''
        headers = ''

        # get html from cache
        html_cache = self.get_html_cache()
        if html_cache:
            headers = html_cache['header']
            html_source = html_cache['body']

        url = self.link

        if self.use_phantom:
            html_source = self.phantom_fetch()

        if not html_source or not self.use_phantom:
            self.fetch_html()
            headers, html_source = self.fetch_html()

        self.set_html_cache(headers=self.headers, content=html_source)
        self.html_source = html_source
        self._headers = headers
        self._referer = url

    def fetch_html(self):
        random_agent = faker.user_agent()
        try:
            response = requests.get(self.link,
                                    headers={'User-Agent': random_agent})
            headers = response.headers
            html_source = response.content
            return headers, html_source
        except Exception, e:
            log.error(e.message)
            raise

    def phantom_fetch(self, timeout=15):
        timeout = self.timeout or timeout
        data = {'url': self.link,
                'expected_element': self.expected_element,
                'timeout': timeout}
        result = get_html_source.delay(**data)
        html_source = ''
        try:
            html_source = result.get()
        except WebDriverException, e:
            log.error('[Phantom] WebDriverException. ', self.link, e.message)

        return html_source

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
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.html_source, from_encoding='utf8')
        return self._soup

    def get_origin_id(self):
        raise NotImplementedError

    @property
    def link(self):
        raise NotImplementedError

    @property
    def images(self):
        raise NotImplementedError

    @property
    def chief_image(self):
        if self._chief_image:
            chief_image = self._chief_image
        else:
            if self._images:
                chief_image = self._images[0]
            else:
                chief_image = self._images[0]
        self._chief_image = chief_image
        return self._chief_image

    @property
    def brand(self):
        raise NotImplementedError

    @property
    def price(self):
        raise NotImplementedError

    @property
    def shop_link(self):
        raise NotImplementedError

    @property
    def shop_nick(self):
        raise NotImplementedError
