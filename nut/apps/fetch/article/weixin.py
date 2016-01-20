#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import os
import random
import sys
import requests

from apps.fetch.article import RequestsTask, Retry


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from urlparse import urljoin, urlparse
from faker import Faker
from django.conf import settings
from celery.task import task
from celery import group
from django.utils.log import getLogger
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout, ConnectionError

from apps.core.models import Article, Media, Authorized_User_Profile
from apps.fetch.common import clean_xml, queryset_iterator


faker = Faker()
IMAGE_DIR = os.path.join(settings.BASE_DIR, 'images')
print IMAGE_DIR
search_api = 'http://weixin.sogou.com/weixinjs'
article_list_api = 'http://weixin.sogou.com/gzhjs'
login_url = 'https://account.sogou.com/web/login'
account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
FETCH_INTERVAL = 1
log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)


class WeiXinClient(requests.Session):
    def __init__(self):
        super(WeiXinClient, self).__init__()
        self._ext = None
        self.login_url = 'https://account.sogou.com/web/login'
        self.logout_url = 'https://account.sogou.com/web/logout_js?client_id=2006'
        self.account_url = 'https://account.sogou.com/web/userinfo/getuserinfo'
        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
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
                ext=False,
                format_json=False):
        if ext:
            params['ext'] = self.ext
        try:
            resp = super(WeiXinClient, self).request(method, url, params, data,
                                                     headers, cookies, files, auth,
                                                     timeout, allow_redirects,
                                                     proxies, hooks, stream, verify,
                                                     cert, json)
        except ConnectionError:
            raise Retry
        except ReadTimeout:
            raise Retry
        if stream:
            return resp
        if not self.cookies:
            self.login()
        result = resp.content.decode('utf-8')
        result = result.rstrip('\n')
        if result.find(u'当前请求已过期') >= 0:
            self.login()
            self.get_ext()
            log.warning(u'ext不正确. url: %s', url)
            raise Retry
        elif result.find(u'您的访问过于频繁') >= 0:
            log.warning(u'访问的过于频繁. url: %s', url)
            self.logout()
            self.login()
            raise Retry(7200)
        if format_json:
            result = self.json_response(resp)
            if 'code' in result and result['code'] == "needlogin":
                self.login()
                raise Retry
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
        username = random.choice(settings.SOGOU_USERS)
        password = settings.SOGOU_PASSWORD
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
        self.request('POST',
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


weixin_client = WeiXinClient()


@task(base=RequestsTask, name='crawl_sogou_articles')
def crawl_articles():
    all_authorized_user = Authorized_User_Profile.objects.\
        filter(weixin_id__isnull=False)
    for user in queryset_iterator(all_authorized_user):
        get_user_articles.delay(user)


@task(base=RequestsTask, name='get_user_articles')
def get_user_articles(gk_user):
    if gk_user.weixin_openid:
        open_id = gk_user.open_id
    else:
        open_id = get_open_id(gk_user.weixin_id)
        gk_user.open_id = open_id
        gk_user.save()

    # get total pages number first
    total_pages = get_list_total_pages(open_id)
    print '> Start to crawl articles of %s. Total pages %d.' % \
          (gk_user.weixin_id, total_pages)
    for page in xrange(1, total_pages + 1):
        fetch_article_list.delay(gk_user, page)


@task(base=RequestsTask, name='fetch_article_list')
def fetch_article_list(gk_user, page=1):
    params = {'openid': gk_user.open_id, 'page': page}
    response = weixin_client.request("GET", article_list_api,
                                     params=params,
                                     ext=True,
                                     format_json=True)
    article_items = response['items']
    for article_item in article_items:
        get_article(article_item, gk_user)


def get_article(article_item, gk_user):
    article_item_xml = clean_xml(article_item)
    article_item_xml = BeautifulSoup(article_item_xml, 'xml')
    cover = article_item_xml.imglink.string
    if cover:
        image_result = fetch_article_images.delay(cover)
        cover = image_result.get()
    article_link = article_item_xml.url.string
    article_data = {'cover': cover}
    crawl_article.delay(article_link, gk_user, article_data)


@task(base=RequestsTask, name='crawl_article')
def crawl_article(article_link, gk_user, article_data):
    try:
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
                            creator=gk_user.user,
                            publish=Article.published
                            )
        article_info.update(article_data)
        if 'cover' not in article_info or not article_info['cover']:
            article_info['cover'] = chief_image
        article = Article(**article_info)
        article.save()
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

        fetch_images = group(fetch_article_images.s(img_src)
                             for img_src in img_src_list)
        image_urls = fetch_images.delay().get()
        for img_tag, img_url in zip(image_tags, image_urls):
            img_tag['src'] = img_url
            img_tag['data-src'] = img_url
        content_html = content.decode_contents(formatter="html")
    chief_image = img_src_list[0] if img_src_list else ''
    return chief_image, content_html


def get_open_id(weixin_id):
    result = fetch_open_id.delay(weixin_id)
    total_pages, open_id = result.get()
    if not open_id:
        for page in xrange(2, total_pages + 1):
            result = fetch_open_id.delay(weixin_id)
            total_pages, open_id = result.get()
            if open_id:
                break
    return open_id


@task(base=RequestsTask, name='fetch_open_id')
def fetch_open_id(weixin_id, page=1):
    open_id = None
    total_pages = 1
    params = dict(type='1', ie='utf8', query=weixin_id, page=page)
    response = weixin_client.request('GET',
                                     url=search_api,
                                     params=params,
                                     format_json=True)
    for item in response['items']:
        item_xml = clean_xml(item)
        item_xml = BeautifulSoup(item_xml, 'xml')
        if item_xml.weixinhao.string == weixin_id:
            open_id = item_xml.id.string
            break
    if page == 1:
        total_pages = int(response['totalPages'])
    return open_id, total_pages


def get_list_total_pages(open_id):
    params = {'openid': open_id}
    response = weixin_client.request("GET", article_list_api,
                                     params=params,
                                     ext=True,
                                     format_json=True)
    total_pages = int(response['totalPages'])
    return total_pages


@task(base=RequestsTask, name='fetch_article_images')
def fetch_article_images(image_url):
    from apps.core.utils.image import HandleImage
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
    crawl_articles.delay()
