#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep

import requests

from bs4 import BeautifulSoup
from faker import Faker


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

faker = Faker()


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


class WeChatArticle(object):
    def __init__(self, we_chat_id, we_chat_name=None):
        self.we_chat_id = we_chat_id
        self.we_chat_name = we_chat_name

        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.articles_api_url = 'http://weixin.sogou.com/gzhjs'

        self.__ext = None
        self.__open_id = None
        self.__headers = None

    @property
    def headers(self):
        if not self.__headers:
            self.__headers = faker.user_agent()
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
                                headers={'UserAgent': self.headers,
                                         'Referer': 'http://weixin.sogou.com/gzhjs?openid=oIWsFtyGRm3FRZuQbcDquZOI5N_E&ext=OVYz1E9f6Gt5FGRk_uyaS3KVGUGG7_T36lFlj3QAjhzRTxfkv-uNb06TRTVsdBB3&cb=sogou.weixin_gzhcb&page=1&',
                                         'Cookie': 'SUID=15C2C23C4418920A0000000056188452; SUV=00452E91726FA77D562CADD6CB4F4317; CXID=5EA449CB6EE00CF81A5B306EF225746E; ssuid=309320514; ad=MrpZFyllll2Qa3TmlllllVB@AzllllllzAKWayllll9lllllpZlll5@@@@@@@@@@; ld=ayllllllll2QWOmTlllllVzjwh9lllllNU@oikllll9lllll4voll5@@@@@@@@@@; ABTEST=0|1451369253|v1; weixinIndexVisited=1; IPLOC=CN1100; SNUID=0B799695E8EDC02489C18394E9E07165; wapsogou_qq_nickname=; sct=23; PHPSESSID=mlnvb0bpj4hjeecr127r1pdih1; SUIR=0B799695E8EDC02489C18394E9E07165; seccodeRight=success; successCount=1|Fri, 08 Jan 2016 10:17:02 GMT; refresh=1',
                                         })

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
                                headers={'UserAgent': self.headers,
                                         'Referer': 'http://weixin.sogou.com/gzhjs?openid=oIWsFtyGRm3FRZuQbcDquZOI5N_E&ext=OVYz1E9f6Gt5FGRk_uyaS3KVGUGG7_T36lFlj3QAjhzRTxfkv-uNb06TRTVsdBB3&cb=sogou.weixin_gzhcb&page=1&',
                                         'Cookie': 'SUID=15C2C23C4418920A0000000056188452; SUV=00452E91726FA77D562CADD6CB4F4317; CXID=5EA449CB6EE00CF81A5B306EF225746E; ssuid=309320514; ad=MrpZFyllll2Qa3TmlllllVB@AzllllllzAKWayllll9lllllpZlll5@@@@@@@@@@; ld=ayllllllll2QWOmTlllllVzjwh9lllllNU@oikllll9lllll4voll5@@@@@@@@@@; ABTEST=0|1451369253|v1; weixinIndexVisited=1; IPLOC=CN1100; SNUID=0B799695E8EDC02489C18394E9E07165; wapsogou_qq_nickname=; sct=23; PHPSESSID=mlnvb0bpj4hjeecr127r1pdih1; SUIR=0B799695E8EDC02489C18394E9E07165; seccodeRight=success; successCount=1|Fri, 08 Jan 2016 10:17:02 GMT; refresh=1',
                                         })

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
        # print result

        total_pages = int(result['totalPages'])
        for page in xrange(2, total_pages + 1):
            params = dict(type='1', ie='utf8', openid=self.open_id, page=page,
                          ext=self.ext, cb='sogou.weixin_gzhcb')
            response = requests.get(url=self.articles_api_url,
                                    params=params,
                                    headers={'UserAgent': self.headers,
                                             'Referer': 'http://weixin.sogou.com/gzhjs?openid=oIWsFtyGRm3FRZuQbcDquZOI5N_E&ext=OVYz1E9f6Gt5FGRk_uyaS3KVGUGG7_T36lFlj3QAjhzRTxfkv-uNb06TRTVsdBB3&cb=sogou.weixin_gzhcb&page=1&',
                                             'Cookie': 'SUID=15C2C23C4418920A0000000056188452; SUV=00452E91726FA77D562CADD6CB4F4317; CXID=5EA449CB6EE00CF81A5B306EF225746E; ssuid=309320514; ad=MrpZFyllll2Qa3TmlllllVB@AzllllllzAKWayllll9lllllpZlll5@@@@@@@@@@; ld=ayllllllll2QWOmTlllllVzjwh9lllllNU@oikllll9lllll4voll5@@@@@@@@@@; ABTEST=0|1451369253|v1; weixinIndexVisited=1; IPLOC=CN1100; SNUID=0B799695E8EDC02489C18394E9E07165; wapsogou_qq_nickname=; sct=23; PHPSESSID=mlnvb0bpj4hjeecr127r1pdih1; SUIR=0B799695E8EDC02489C18394E9E07165; seccodeRight=success; successCount=1|Fri, 08 Jan 2016 10:17:02 GMT; refresh=1',
                                             })

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
            sleep(3)

    def fetch_article(self):
        pass

    def request_url(self, url, params):
        # Todo(judy): add reference
        pass


if __name__ == '__main__':
    wechat = WeChatArticle('shenyebagua818')
    print '> open id: ', wechat.open_id
    print '> ext: ', wechat.ext
    print '> articles: '
    wechat.get_article_list()
