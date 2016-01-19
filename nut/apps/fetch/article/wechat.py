#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

import json
import time
import urllib
import redis
import requests

from time import sleep
from faker import Faker
from bs4 import BeautifulSoup
from django.conf import settings

from apps.fetch.common import process_eqs, process_jsonp, get_key, get_cookies, \
    clean_xml, parse_article_link
from settings import WEIXIN_URL
from apps.core.models import Article, GKUser


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

faker = Faker()
r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


class WeChat(object):
    def __init__(self, we_chat_id, we_chat_name=None):
        self.we_chat_id = we_chat_id
        self.we_chat_name = we_chat_name

        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.articles_api_url = 'http://weixin.sogou.com/gzhjs'
        self.login_url = 'https://account.sogou.com/web/login'
        self.account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
        self.total_pages = 1
        self.article_link_list = []

        self.__ext = None
        self.__open_id = None
        self.__headers = None
        self._cookie = None
        self.session_request = requests.Session()

    @property
    def headers(self):
        if not self.__headers:
            headers = {'UserAgent': faker.user_agent()}
            self.__headers = headers
        return self.__headers

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
        ext_id = None
        open_id = None
        for item in items:
            item = clean_xml(item)
            item_soup = BeautifulSoup(item, 'xml')
            if item_soup.weixinhao.string == self.we_chat_id:
                ext_id = item_soup.ext.string.strip()
                open_id = item_soup.id.string.strip()
                break
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
        response = self.session_request.get(url=self.search_api_url,
                                            params=params)

        source_result = response.content.rstrip('\n')
        if source_result.startswith('weixin('):
            source_result = source_result[7:-1]
        result = json.loads(source_result)
        return result

    def get_article_list(self, page=1):
        params = {'openid': self.open_id,
                  'ext': self.ext}
        response = self.session_request.request("GET", self.articles_api_url,
                                                params=params)
        source_result = response.text.rstrip('\n')
        if source_result.startswith('sogou.weixin_gzhcb('):
            source_result = source_result[19:-1]
        result = json.loads(source_result)
        sleep(10)
        if page == 1:
            self.total_pages = int(result['totalPages'])
        return self.total_pages, result

    def crawl_article(self, article_link):
        response = self.session_request.get(url=article_link)
        html_source = response.content.decode('utf-8')
        article_soup = BeautifulSoup(html_source)

        title = article_soup.select('h2.rich_media_title')[0].text
        published_time = article_soup.select('em#post-date')[0].text
        content = article_soup.select('id#js_content')[0].string
        author = article_soup.select('span.rich_media_meta_nickname')[0].text
        qr_code = article_soup.select('img#js_pc_qr_code_img')[0].attrs.get(
            'src')
        print title
        print published_time
        print author
        print content[:100]
        print qr_code

        creator = GKUser.objects.get(pk=1)
        article = Article(title=title,
                          creator=creator,
                          content=content,
                          created_datetime=published_time,
                          publish=Article.draft,
                          )
        article.save()

    def crawl(self):
        self.login()
        total_pages, result = self.get_article_list()
        # article_link_list = parse_article_link(result)

        article_link_list = []
        for article in result['items']:
            article_instance = Article()
            article_xml = clean_xml(article)
            article_soup = BeautifulSoup(article_xml, 'xml')
            article_link_list.append(
                'http://weixin.sogou.com' + article_soup.url.string)
            article_instance.title = article_soup.title1.string
            article_instance.cover = article_soup.imglink
            print '        * ', article_soup.title1.string

        for link in article_link_list:
            print link
            self.crawl_article(link)

            # for page in xrange(2, total_pages+1):
            #     total_pages, result = self.get_article_list(page)
            #     article_link_list = parse_article_link(result)
            #     for link in article_link_list:
            #         self.crawl_article(link)

    def login(self):
        username = settings.SOUGOU_EMAIL
        password = settings.SOUGOU_PASSWORD
        headers = {
            'Referer': 'https://account.sogou.com/web/webLogin',
            'Origin': 'Origin:https://account.sogou.com',
            'Host': 'account.sogou.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        for k, v in self.headers.items():
            headers.setdefault(k, v)

        data = dict(username=username,
                    password=password,
                    autoLogin=1,
                    client_id='2006',
                    xd='http://news.sogou.com/jump.htm',
                    )
        self.session_request.post(self.login_url, data=data,
                                  headers=headers)
        assert self.session_request.get(self.account_url).status_code == 200


if __name__ == '__main__':
    wechat = WeChat('shenyebagua818')
    print '> articles: '
    print wechat.crawl()
    print '>> happy ending!'
