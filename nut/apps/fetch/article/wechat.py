#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup
from faker import Faker


faker = Faker()


class WeChatArticle(object):
    def __init__(self, we_chat_id, we_chat_name=None, open_id=None):
        self.open_id = open_id
        self.we_chat_id = we_chat_id
        self.we_chat_name = we_chat_name

        self.search_url = 'http://weixin.sogou.com/weixin'
        self.base_url = 'http://weixin.sogou.com'

        self.search_page = None
        self.headers = None

    @property
    def account_list_url(self):
        soup = BeautifulSoup(self.search_page)
        account_id_tags = soup.find_all('label', attrs={'name': 'em_weixinhao'})
        account_id_tag = None
        if account_id_tags:
            for tag in account_id_tags:
                if tag.text.find(self.we_chat_id) >= 0:
                    account_id_tag = tag
                    break

        if not account_id_tag:
            # Todo(judy): Return some notifications.
            pass

        if account_id_tag:
            list_tag = account_id_tag.\
                find_parents('div',
                             attrs={'class': 'wx-rb bg-blue wx-rb_v1 _item'})

            list_url = self.base_url + list_tag[0].attrs['href']
            return list_url

    def get_search_page(self):
        html_source = ''
        if not self.open_id:
            params = dict(type='1', ie='utf8', query=self.we_chat_id)
            headers = faker.user_agent()
            response = requests.get(url=self.search_url,
                                    params=params,
                                    headers={'UserAgent': headers})
            html_source = response.content.decode('utf8')
        self.search_page = html_source

