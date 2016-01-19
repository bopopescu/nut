#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import random
import sys
import requests


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from faker import Faker
from django.conf import settings
from celery.task import task
from django.utils.log import getLogger
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup

from apps.core.models import Article, GKUser
from apps.fetch.common import clean_xml
from apps.core.tasks import BaseTask


faker = Faker()
search_api = 'http://weixin.sogou.com/weixinjs'
article_list_api = 'http://weixin.sogou.com/gzhjs'
login_url = 'https://account.sogou.com/web/login'
account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
FETCH_INTERVAL = 10
log = getLogger('django')


class WeiXinClient(requests.Session):
    def __init__(self, format_json=True):
        super(WeiXinClient, self).__init__()
        self._ext = None
        self.login_url = 'https://account.sogou.com/web/login'
        self.account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.format_json = format_json

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None,
                ext=False):
        if ext:
            params['ext'] = self.ext
        if not headers:
            headers = {'UserAgent': faker.user_agent(),
                       'Referer': 'http://weixin.sogou.com/'}
        else:
            headers['UserAgent'] = faker.user_agent()
        resp = super(WeiXinClient, self).request(method, url, params, data,
                                                 headers, cookies, files, auth,
                                                 timeout, allow_redirects,
                                                 proxies, hooks, stream, verify,
                                                 cert, json)
        if not self.cookies:
            self.login()
        result = resp.content.decode('utf-8')
        result = result.rstrip('\n')
        if result.find(u'当前请求已过期') >= 0:
            self.login()
            self.get_ext()
            raise FetchError
        elif result.find(u'您的访问过于频繁') >= 0:
            sleep(3600)
        if self.format_json:
            result = self.json_response(resp)
            if 'code' in result and result['code'] == "needlogin":
                self.login()
                raise FetchError
        sleep(FETCH_INTERVAL)
        return result

    @property
    def ext(self):
        if not self._ext:
            self.get_ext()
        return self._ext

    def get_ext(self):
        any_word = random.choice('abcdefghijklmnopqrstuvwxyz')
        params = dict(type='1', ie='utf8', query=any_word, page=1)
        item_list = self.get(url=self.search_api_url, params=params)['items']
        account_xml = clean_xml(item_list[0])
        account_xml = BeautifulSoup(account_xml, 'xml')
        self._ext = account_xml.ext.string

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
        data = dict(username=username,
                    password=password,
                    autoLogin=1,
                    client_id='2006',
                    xd='http://news.sogou.com/jump.htm',
                    )
        self.format_json = False
        self.request('POST',
                     self.login_url, data=data, headers=headers)
        assert self.get(self.account_url).status_code == 200

    @classmethod
    def json_response(cls, response):
        result = response.content.decode('utf-8')
        result = result.rstrip('\n')
        if result.startswith('weixin('):
            result = result[7:-1]
        elif result.startswith('sogou.weixin_gzhcb('):
            result = result[19:-1]
        try:
            return json.loads(result)
        except ValueError:
            return result


class FetchError(Exception):
    def __init__(self):
        self.message = 'Fetch error, need to login or get new token.'


weixin_client = WeiXinClient()


def crawl_we_chat_articles():
    weixin_id_list = {1: {'weixin_id': 'shenyebagua818', 'id': 1},
                      2: {'weixin_id': 'cctvnewscenter', 'id': 2},
                      3: {'weixin_id': 'bb2b2bb', 'id': 3},
                      4: {'weixin_id': 'a529597', 'id': 4},
                      5: {'weixin_id': 'woshitongdao', 'id': 5}}
    for item in weixin_id_list.items():
        get_article_list(item[1])


def get_article_list(gk_user):
    # if gk_user.open_id:
    if 'open_id' in gk_user and gk_user['open_id']:
        # open_id = gk_user.open_id
        open_id = gk_user['open_id']
    else:
        open_id = get_open_id(gk_user['weixin_id'])
        # gk_user.open_id = open_id
        gk_user['open_id'] = open_id

    total_pages, article_items = _get_article_list(open_id)
    for article_item in article_items:
        get_article(article_item, gk_user)

    if total_pages > 1:
        for page in xrange(2, total_pages + 1):
            total_pages, article_items = _get_article_list(open_id, page)

            for article_item in article_items:
                get_article(article_item, gk_user)


def _get_article_list(open_id, page=1):
    total_pages = 0
    params = {'openid': open_id, 'page': page}
    response = weixin_client.request("GET", article_list_api,
                                     params=params, ext=True)
    if page == 1:
        total_pages = int(response.totalPages.string)
    return total_pages, response


def get_article(article_item, gk_user):
    article_item_xml = clean_xml(article_item)
    article_item_xml = BeautifulSoup(article_item_xml, 'xml')
    title = article_item_xml.title1.string or article_item_xml.title.string
    gkuser = GKUser.objects.get(pk=gk_user['id'])
    cover_image = article_item_xml.imglink.string
    gkuser.head_image = article_item_xml.headimage.string
    create_date = datetime.strptime(article_item_xml.date.string, '%Y-%m-%d')
    article_data = dict(
        title=title,
        creator=gkuser,
        cover_image=cover_image,
        created_datetime=create_date,
        updated_datetime=create_date
    )
    article_link = article_item_xml.url.string
    article_info = crawl_article(article_link)
    article_info.update(article_data)
    Article(**article_info)


def crawl_article(article_link):
    weixin_client.format_json = False
    html_source = weixin_client.get(url=article_link)
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

    article_info = dict(title=title,
                        content=content,
                        created_datetime=published_time,
                        publish=Article.draft
                        )
    return article_info


def get_open_id(weixin_id):
    total_pages, open_id = _get_open_id(weixin_id)
    if not open_id:
        for page in xrange(2, total_pages + 1):
            total_pages, open_id = _get_open_id(weixin_id)
            if open_id:
                break
    return open_id


def _get_open_id(weixin_id, page=1):
    total_pages = 1
    open_id = None

    params = dict(type='1', ie='utf8', query=weixin_id, page=page)
    response = weixin_client.request('GET',
                                     url=search_api, params=params)
    for item in response['items']:
        item_xml = clean_xml(item)
        item_xml = BeautifulSoup(item_xml, 'xml')
        if item_xml.weixinhao.string == weixin_id:
            open_id = item_xml.id.string
            break
    if not open_id and page == 1:
        total_pages = int(response.totalPages.string)
    return total_pages, open_id


if __name__ == '__main__':
    crawl_we_chat_articles()
