#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import random
import sys
from urlparse import urljoin, urlparse

import requests
from requests.exceptions import ReadTimeout, ConnectionError

from apps.fetch.article import RequestsTask


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from faker import Faker
from django.conf import settings
from celery.task import task
from celery import group
from django.utils.log import getLogger
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
IMAGE_DIR = os.path.join(settings.BASE_DIR, 'images')
print IMAGE_DIR

from apps.core.models import Article, GKUser, Media
from apps.fetch.common import clean_xml


faker = Faker()
search_api = 'http://weixin.sogou.com/weixinjs'
article_list_api = 'http://weixin.sogou.com/gzhjs'
login_url = 'https://account.sogou.com/web/login'
account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
FETCH_INTERVAL = 10
log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)


raise TypeError

class WeiXinClient(requests.Session):
    def __init__(self, format_json=True):
        super(WeiXinClient, self).__init__()
        self._ext = None
        self.login_url = 'https://account.sogou.com/web/login'
        self.logout_url = 'https://account.sogou.com/web/logout_js?client_id=2006'
        self.account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.format_json = format_json
        self._headers = ''

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
        try:
            resp = super(WeiXinClient, self).request(method, url, params, data,
                                                     headers, cookies, files, auth,
                                                     timeout, allow_redirects,
                                                     proxies, hooks, stream, verify,
                                                     cert, json)
        except ConnectionError:
            raise FetchError
        except ReadTimeout:
            raise FetchError
        if not self.cookies:
            self.login()
        if stream:
            return resp
        result = resp.content.decode('utf-8')
        result = result.rstrip('\n')
        if result.find(u'当前请求已过期') >= 0:
            self.login()
            self.get_ext()
            raise FetchError
        elif result.find(u'您的访问过于频繁') >= 0:
            self.logout()
            self.login()
            raise FetchError
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
        username = random.choice(settings.SOUGOU_USERS)
        password = settings.SOUGOU_PASSWORD
        headers = {
            'Referer': 'http://news.sogou.com/?p=40030300&kw=',
            'Origin': 'http://news.sogou.com',
            'Host': 'account.sogou.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'RA-Sid': '77094B42-20140626-080311-ac7a24-cf2748',
            'RA-Ver': '3.0.7',
            'Upgrade-Insecure-Requests': 1,
            'UserAgent': faker.user_agent(),
        }
        data = dict(username=username,
                    password=password,
                    autoLogin=1,
                    client_id='2006',
                    xd='http://news.sogou.com/jump.htm',
                    )
        self.format_json = False
        resp = self.request('POST',
                     self.login_url, data=data, headers=headers)

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

    def logout(self):
        self.get(self.logout_url)


class FetchError(Exception):
    def __init__(self):
        self.message = 'Fetch error, need to login or get new token.'


weixin_client = WeiXinClient()


def crawl_we_chat_articles():
    weixin_id_list = {1: {'weixin_id': 'shenyebagua818', 'id': 1},
                      2: {'weixin_id': 'cctvnewscenter', 'id': 2},
                      3: {'weixin_id': 'bb2b2bb', 'id': 3},
                      4: {'weixin_id': 'a529597', 'id': 4},
                      5: {'weixin_id': 'woshitongdao', 'id': 5},
                      6: {'weixin_id': 'vicechina', 'id': 6},
                      }
    for item in weixin_id_list.items():
        get_article_list(item[1])


def get_article_list(gk_user):
    print '> start to fetch user: %s.' % gk_user['weixin_id']
    # if gk_user.open_id:
    if 'open_id' in gk_user and gk_user['open_id']:
        # open_id = gk_user.open_id
        open_id = gk_user['open_id']
    else:
        open_id = get_open_id(gk_user['weixin_id'])
        # gk_user.open_id = open_id
        gk_user['open_id'] = open_id

    total_pages = get_list_total_pages(open_id)
    for page in xrange(1, total_pages + 1):
        _get_article_list.delay(open_id, gk_user, page)


@task(base=RequestsTask)
def _get_article_list(open_id, gk_user, page=1):
    # 合并后不需要再传open_id,而是从gk_user里取.
    print '    page: %s' % page
    params = {'openid': open_id, 'page': page}
    try:
        weixin_client.format_json = True
        response = weixin_client.request("GET", article_list_api,
                                         params=params, ext=True)
        article_items = response['items']
        for article_item in article_items:
            get_article(article_item, gk_user)

    except FetchError, e:
        _get_article_list.retry(exc=e, countdown=30)
        # _get_article_list.retry(xargs={'open_id': open_id,
        #                                'gk_user': gk_user,
        #                                'page': page},
        #                         exc=e, countdown=30)


def get_article(article_item, gk_user):
    article_item_xml = clean_xml(article_item)
    article_item_xml = BeautifulSoup(article_item_xml, 'xml')
    gkuser = GKUser.objects.get(pk=gk_user['id'])
    cover = article_item_xml.imglink.string
    if cover:
        image_result = fetch_article_image.delay(cover)
        cover = image_result.get()
    article_link = article_item_xml.url.string
    article_data = {'cover': cover}
    crawl_article.delay(article_link, gkuser, article_data)


@task(base=RequestsTask)
def crawl_article(article_link, gkuser, article_data):
    try:
        weixin_client.format_json = False
        url = urljoin('http://weixin.sogou.com/', article_link)
        html_source = weixin_client.request('GET', url=url)
        article_soup = BeautifulSoup(html_source)

        title = article_soup.select('h2.rich_media_title')[0].text
        published_time = article_soup.select('em#post-date')[0].text
        published_time = datetime.strptime(published_time, '%Y-%m-%d')
        content = article_soup.find('div', id='js_content')
        author = article_soup.select('span.rich_media_meta_nickname')[0].text
        qr_code = article_soup.select('img#js_pc_qr_code_img')[0].attrs.get(
            'src')
        print '-' * 80
        print '        ', title
        print '        ', published_time
        print '        ', author
        print '        ', content
        print '        ', qr_code
        print
        print
        print

        chief_image, content = parse_article_content(content)
        article_info = dict(title=title,
                            content=content,
                            created_datetime=published_time,
                            creator=gkuser,
                            publish=Article.published
                            )
        article_info.update(article_data)
        if 'cover' not in article_info or not article_info['cover']:
            article_info['cover'] = chief_image
        article = Article(**article_info)
        article.save()
    except FetchError, e:
        # crawl_article.retry(xargs={'article_link': article_link,
        #                            'gkuer':gkuser,
        #                            'article_data':article_data},
        #                         exc=e, countdown=30)
        crawl_article.retry(exc=e, countdown=30)
    except BaseException, e:
        log.error(e.message)


def parse_article_content(content):
    image_tags = content.find_all('img')
    img_src_list = []
    content_html = ''
    if image_tags:
        for image_tag in image_tags:
            img_src = image_tag.attrs.get('src')
            if not img_src:
                img_src = image_tag.attrs.get('data-src')
            if img_src:
                img_src_list.append(img_src)

        # fetch_images = group(fetch_article_image.s(img_src_list))
        fetch_images = group(fetch_article_image.s(img_src)
                             for img_src in img_src_list)
        image_urls = fetch_images.delay().get()
        for img_tag, img_url in zip(image_tags, image_urls):
            img_tag['src'] = img_url
            img_tag['data-src'] = img_url
        content_html = content.decode_contents(formatter="html")
    chief_image = img_src_list[0] if img_src_list else ''
    return chief_image, content_html


def get_open_id(weixin_id):
    total_pages, open_id = _get_open_id(weixin_id)
    if not open_id:
        for page in xrange(2, total_pages + 1):
            total_pages, open_id = _get_open_id(weixin_id)
            if open_id:
                break
    return open_id


def _get_open_id(weixin_id, page=1):
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
    return open_id
    # except FetchError, e:
        # _get_open_id.retry(xargs={'weixin_id': weixin_id, 'page': page},
        #                         exc=e, countdown=30)
        # _get_open_id.retry(exc=e, countdown=30)


def get_list_total_pages(open_id):
    params = {'openid': open_id}
    try:
        weixin_client.format_json = True
        response = weixin_client.request("GET", article_list_api,
                                         params=params, ext=True)
        total_pages = int(response['totalPages'])
        return total_pages
    except FetchError:
        return get_list_total_pages(open_id)


from apps.core.tasks import BaseTask
from apps.core.utils.image import HandleImage


@task(base=RequestsTask)
def fetch_article_image(image_url):
    image_url = fix_image_url(image_url)
    r = requests.get(image_url, stream=True)
    image_full_name = ''
    try:
        image = HandleImage(r.raw)
        image_name = image.save(path=IMAGE_DIR)
        image_full_name = "%s%s" % (image_host, image_name)
        Media.objects.create(
            file_path=image_name,
            content_type=getattr(image, 'content_type', 'image/jpeg')
        )
    except BaseException, e:
        log.error(e.message)
    except AttributeError, e:
        log.error(e.message)
    return image_full_name


def fix_image_url(image_url):
    url_parts = urlparse(image_url)
    path_parts = url_parts.path.split('/')
    if path_parts[-1] == '0':
        fix_path = '/'.join(path_parts[:-1])
        if not fix_path.endswith('/'):
            fix_path += '/'
        image_url = url_parts._replace(path=fix_path).geturl()
    return image_url


if __name__ == '__main__':
    crawl_we_chat_articles()
