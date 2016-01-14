#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys



BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

import json
import random
import time
import urllib
import redis
import requests

from time import sleep
from faker import Faker
from bs4 import BeautifulSoup
from django.conf import settings

from apps.core.tasks import get_cookies
from apps.fetch.common import process_eqs, process_jsonp
from settings import WEIXIN_KEY, WEIXIN_URL


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

faker = Faker()
r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


def clean_xml(xml_str):
    replaces = (
        ('<?xml version="1.0" encoding="gbk"?>',
         '<xml version="1.0" encoding="gbk">'),
        ('\\', ''),)

    for from_str, to_str in replaces:
        xml_str = xml_str.replace(from_str, to_str)

    if not xml_str.endswith('</xml>'):
        xml_str += '</xml>'

    return xml_str


class WeChat(object):
    def __init__(self, we_chat_id, we_chat_name=None):
        self.we_chat_id = we_chat_id
        self.we_chat_name = we_chat_name

        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.articles_api_url = 'http://weixin.sogou.com/gzhjs'

        self.__ext = None
        self.__open_id = None
        self.__headers = None
        self._cookie = None

    @property
    def headers(self):
        if not self.__headers:
            headers = {'UserAgent': faker.user_agent(),
                     'Referer': 'http://weixin.sogou.com/gzhjs?openid=oIWsFtyGRm3FRZuQbcDquZOI5N_E&ext=OVYz1E9f6Gt5FGRk_uyaS3KVGUGG7_T36lFlj3QAjhzRTxfkv-uNb06TRTVsdBB3&cb=sogou.weixin_gzhcb&page=1&',
                     'Cookie': self.cookie,
                     }
            self.__headers = headers
        return self.__headers

    @property
    def cookie(self):
        if not self._cookie:
            cookie = get_cookies('we_chat')
            self._cookie = cookie
        return self._cookie

    @property
    def ext(self):
        if not self.__ext:
            self.get_keys()
        return self.__ext

    @property
    def open_id(self):
        if not self.__open_id:
            self.get_keys()
        return self.__open_id

    def get_keys(self):
        result = self.fetch_search_page()
        items = result['items']
        open_id, ext_id = self.parse_id_and_ext(items)
        found = (open_id and ext_id)
        if found:
            self.__open_id = open_id
            self.__ext = ext_id
            return

        total_pages = int(result['totalPages'].string)
        for page in xrange(2, total_pages + 1):
            result = self.fetch_search_page(page=page)
            items = result['items']
            open_id, ext_id = self.parse_id_and_ext(items)
            found = open_id and ext_id
            if found:
                self.__open_id = open_id
                self.__ext = ext_id
                return

    def parse_id_and_ext(self, item_list):
        open_id = None
        ext_id = None
        for item in item_list:
            item = clean_xml(item)
            item_soup = BeautifulSoup(item, 'xml')
            if item_soup.weixinhao.string == self.we_chat_id:
                ext_id = item_soup.ext.string.strip()
                open_id = item_soup.id.string.strip()
                break
        return open_id, ext_id

    def fetch_search_page(self, page=1):
        params = dict(type='1', ie='utf8', query=self.we_chat_id, page=page)
        response = requests.get(url=self.search_api_url,
                                params=params,
                                headers=self.headers)

        source_result = response.content.rstrip('\n')
        if source_result.startswith('weixin('):
            source_result = source_result[7:-1]
        result = json.loads(source_result)
        return result

    def get_article_list(self, page=1):
        params = dict(type='1', ie='utf8', openid=self.open_id, page=page,
                      ext=self.ext, cb='sogou.weixin_gzhcb')
        response = requests.get(url=self.articles_api_url,
                                params=params,
                                headers=self.headers)

        source_result = response.content.rstrip('\n')
        if source_result.startswith('sogou.weixin_gzhcb('):
            source_result = source_result[19:-1]
        result = json.loads(source_result)
        print '    page: 1'
        for article in result['items']:
            article = clean_xml(article)
            article_soup = BeautifulSoup(article, 'xml')
            print '        * ', article_soup.title1.string
        print ''
        sleep(3)

        total_pages = int(result['totalPages'])
        for page in xrange(2, total_pages + 1):
            params = dict(type='1', ie='utf8', openid=self.open_id, page=page,
                          ext=self.ext, cb='sogou.weixin_gzhcb')
            response = requests.get(url=self.articles_api_url,
                                    params=params,
                                    headers=self.headers)

            source_result = response.content.rstrip('\n')
            if source_result.startswith('sogou.weixin_gzhcb('):
                source_result = source_result[19:-1]
            result = json.loads(source_result)
            print '    page: ', page
            for article in result['items']:
                article = clean_xml(article)
                article_soup = BeautifulSoup(article, 'xml')
                print '        * ', article_soup.title1.string
            print ''
            sleep(10)

    def fetch_article(self):
        pass

    def request_url(self, url, params):
        # Todo(judy): add reference
        pass

    def craw_article(self, article_link):
        # get article
        sleep(10)
        response = requests.get(url=article_link, headers=self.headers)
        return response

    def crawl(self):
        headers = self.headers
        open_id = self.open_id

        key = r.get('sougou:key')
        eqs = process_eqs(key[0], open_id, key[2])

        url = WEIXIN_URL.format(id=open_id, eqs=urllib.quote(eqs), ekv=key[1], t=int(time.time()*1000)) # 生成api url

        # 访问api url,获取公众号文章列表
        response = requests.get(url=url, headers=headers)

        if not response.status_code == 200:
            # Todo(judy): retry
            pass

        jsonp = response.content.decode('utf-8')
        items = process_jsonp(jsonp)
        for item in items:
            self.craw_article(item['link'])

        if not items:
            pass

        responses = [self.craw_article(i['link']) for i in items]
        for response in responses:
            if response.status_code != 200:
                pass


if __name__ == '__main__':
    wechat = WeChat('shenyebagua818')
    print '> articles: '
    # wechat.get_article_list()
    print wechat.crawl()
    print '>> happy ending!'

