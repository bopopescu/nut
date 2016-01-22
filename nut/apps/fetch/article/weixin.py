#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import random
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from django.conf import settings
from urlparse import urljoin, urlparse
from celery.task import task
from django.utils.log import getLogger
from datetime import datetime
from bs4 import BeautifulSoup

from apps.core.models import Article, Media, Authorized_User_Profile
from apps.fetch.common import clean_xml, queryset_iterator
from apps.fetch.article import RequestsTask, WeiXinClient


SEARCH_API = 'http://weixin.sogou.com/weixinjs'
ARTICLE_LIST_API = 'http://weixin.sogou.com/gzhjs'
log = getLogger('django')
weixin_client = WeiXinClient()
qr_code_patterns = (re.compile('biz\s*=\s*"(?P<qr_url>[^"]*)'),
                    re.compile('fakeid\s*=\s*"(?P<qr_url>[^"]*)'),
                    re.compile('appuin\s*=\s*"(?P<qr_url>[^"]*)'))
image_host = getattr(settings, 'IMAGE_HOST', None)


@task(base=RequestsTask, name='sogou.crawl_articles', rate_limit='5/m')
def crawl_articles():
    all_authorized_user = Authorized_User_Profile.objects. \
        filter(weixin_id__isnull=False)
    for user in queryset_iterator(all_authorized_user):
        gk_user = {'weixin_openid': user.weixin_openid,
                   'weixin_id': user.weixin_id,
                   'pk': user.pk,
                   'weixin_qrcode_img': user.weixin_qrcode_img}
        get_user_articles.delay(gk_user)


@task(base=RequestsTask, name='sogou.get_user_articles', rate_limit='5/m')
def get_user_articles(gk_user):
    open_id, ext = get_open_id(gk_user['weixin_id'])
    gk_user['weixin_openid'] = open_id
    gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
    gk_user_instance.weixin_openid = open_id
    gk_user_instance.save()
    fetch_article_list.delay(gk_user, open_id, ext)


@task(base=RequestsTask, name='sogou.fetch_article_list', rate_limit='5/m')
def fetch_article_list(gk_user, open_id, ext):
    page = 1
    total_pages = 1
    go_next = True

    while go_next:
        params = {'openid': open_id, 'ext': ext, 'page': page}
        response = weixin_client.request("GET", ARTICLE_LIST_API,
                                         params=params,
                                         format_json=True)
        json_items = response['items']
        if total_pages == 1:
            total_pages = int(response['totalPages'])

        item_dict = {}
        for article_item in json_items:
            article_item_xml = clean_xml(article_item)
            article_item_xml = BeautifulSoup(article_item_xml, 'xml')
            article_link = article_item_xml.url.string
            url = urljoin('http://weixin.sogou.com/', article_link)
            item_dict[url] = article_item_xml

        existed = Article.objects.values_list('origin_source'). \
            filter(origin_source__in=item_dict.keys())
        if existed:
            existed = [item[0] for item in existed]
            go_next = False

        article_items = [article_item for url, article_item in item_dict.items()
                         if url not in existed]
        if article_items:
            for article_item in article_items:
                get_article(article_item, gk_user)

        page += 1
        if total_pages == page:
            go_next = False


def get_article(article_item, gk_user):
    cover = article_item.imglink.string
    article_data = dict()
    if cover:
        article_data = {'cover': cover}
    article_link = article_item.url.string
    crawl_article.delay(article_link, gk_user, article_data)


@task(base=RequestsTask, name='sogou.crawl_article', rate_limit='5/m')
def crawl_article(article_link, gk_user, article_data):
    url = urljoin('http://weixin.sogou.com/', article_link)
    html_source = weixin_client.request('GET', url=url)
    article_soup = BeautifulSoup(html_source)
    get_qr_code.delay(gk_user, html_source)

    title = article_soup.select('h2.rich_media_title')[0].text
    published_time = article_soup.select('em#post-date')[0].text
    published_time = datetime.strptime(published_time, '%Y-%m-%d')
    content = article_soup.find('div', id='js_content')
    creator = Authorized_User_Profile.objects.get(pk=gk_user['pk']).user

    article_info = dict(title=title,
                        content=content.decode_contents(formatter="html"),
                        created_datetime=published_time,
                        creator=creator,
                        publish=Article.published,
                        origin_source=url
                        )
    article_info.update(article_data)
    log.info('Insert article. %s', article_info)
    article = Article(**article_info)
    article.save()
    log.info('Insert article. succeed')
    parse_article_content.delay(article.pk)


@task(base=RequestsTask, name='sogou.parse_article_content', rate_limit='5/m')
def parse_article_content(article_id):
    article = Article.objects.get(pk=article_id)
    content = article.content
    cover = article.cover
    if cover:
        cover = fetch_image(cover)
        article.cover = cover
        article.save()

    article_soup = BeautifulSoup(content)
    image_tags = article_soup.find_all('img')
    if image_tags:
        for i, image_tag in enumerate(image_tags):
            img_src = image_tag.attrs.get('src')
            if not img_src:
                img_src = image_tag.attrs.get('data-src')
            if img_src and img_src.find('mmbiz.qpic.cn') >= 0:
                gk_img_rc = fetch_image(img_src)
                if gk_img_rc:
                    image_tag['src'] = gk_img_rc
                    image_tag['data-src'] = gk_img_rc
                    if not cover and i == 0:
                        article.cover = gk_img_rc
            content_html = article_soup.decode_contents(formatter="html")
            article.content = content_html
            article.save()


def get_open_id(weixin_id):
    log.info('get open_id for %s', weixin_id)
    open_id, ext, total_pages = fetch_open_id(weixin_id)
    if not open_id:
        log.warning('cannot find open_id on page 1')
        for page in xrange(2, total_pages + 1):
            open_id, ext, total_pages = fetch_open_id(weixin_id)
            if open_id:
                break
    return open_id, ext


def fetch_open_id(weixin_id, page=1):
    log.info('fetch open_id for %s', weixin_id)
    open_id = None
    ext = None
    total_pages = 1
    params = dict(type='1', ie='utf8', query=weixin_id, page=page)
    response = weixin_client.request('GET',
                                     url=SEARCH_API,
                                     params=params,
                                     format_json=True)
    for item in response['items']:
        item_xml = clean_xml(item)
        item_xml = BeautifulSoup(item_xml, 'xml')
        if item_xml.weixinhao.string == weixin_id:
            open_id = item_xml.id.string
            ext = item_xml.ext.string
            break
    if page == 1:
        total_pages = int(response['totalPages'])
    return open_id, ext, total_pages


def fetch_image(image_url):
    image_full_name = ''
    from apps.core.utils.image import HandleImage
    r = weixin_client.request('GET',
                              url=image_url,
                              stream=True)
    try:
        try:
            content_type = r.headers['Content-Type']
        except KeyError:
            content_type = 'image/jpeg'
        image = HandleImage(r.raw)
        image_name = image.save()
        image_full_name = "%s%s" % (image_host, image_name)
        Media.objects.create(
            file_path=image_name,
            content_type=content_type)
    except BaseException, e:
        print image_url
        log.error('Handle Image Error: %s', e.message)
    return image_full_name


@task(base=RequestsTask, name='sogou.get_qr_code', rate_limit='5/m')
def get_qr_code(gk_user, html_source):
    if not gk_user['weixin_qrcode_img']:
        article_soup = BeautifulSoup(html_source)
        scripts = article_soup.select('script')
        biz = ''
        for script in scripts:
            found = False
            for pattern in qr_code_patterns:
                biz_tag = pattern.findall(script.text)
                if biz_tag:
                    biz = biz_tag[0]
                    found = True
            if found:
                break

        scene = random.randrange(10000001, 10000007)
        qr_code_url = 'http://mp.weixin.qq.com/mp/qrcode?scene=%s&__biz=%s' % \
                      (scene, biz)
        qr_code_image = fetch_image(qr_code_url)

        gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
        gk_user_instance.weixin_qrcode_img = qr_code_image
        gk_user_instance.save()


def fix_image_url(image_url):
    url_parts = urlparse(image_url)
    path_parts = url_parts.path.split('/')
    if path_parts[-1] == '0':
        fix_path = '/'.join(path_parts[:-1])
        query = url_parts.query
        if query:
            query_parts = query.split('&')
            query = [query for query in query_parts if query.startswith('wx_fmt=')][0]
        if not fix_path.endswith('/'):
            fix_path += '/'
        image_url = url_parts._replace(path=fix_path, query=query).geturl()
    return image_url
