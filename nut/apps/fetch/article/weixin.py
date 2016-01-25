#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from wand.exceptions import WandException
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


@task(base=RequestsTask, name='sogou.crawl_articles', rate_limit='1/m')
def crawl_articles():
    all_authorized_user = Authorized_User_Profile.objects. \
        filter(weixin_id__isnull=False)
    for user in queryset_iterator(all_authorized_user):
        gk_user = {'weixin_openid': user.weixin_openid,
                   'weixin_id': user.weixin_id,
                   'pk': user.pk,
                   'weixin_qrcode_img': user.weixin_qrcode_img}
        get_user_articles.delay(gk_user)


@task(base=RequestsTask, name='sogou.get_user_articles', rate_limit='1/m')
def get_user_articles(gk_user):
    open_id, ext, sg_cookie = get_token(gk_user['weixin_id'])
    if not open_id:
        log.warning("skip user %s: cannot find open_id. Is weixin_id correct?",
                    gk_user['weixin_id'])
        return

    gk_user['weixin_openid'] = open_id
    gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
    gk_user_instance.weixin_openid = open_id
    gk_user_instance.save()
    fetch_article_list.delay(gk_user=gk_user, open_id=open_id, ext=ext,
                             sg_cookie=sg_cookie)


@task(base=RequestsTask, name='sogou.fetch_article_list', rate_limit='1/m')
def fetch_article_list(gk_user, open_id, ext, sg_cookie, page=1):
    print
    print
    print '-' * 80
    print sg_cookie
    print '-' * 80
    print
    print
    go_next = True
    params = {
        'openid': open_id,
        'ext': ext,
        'page': page,
        'cb': 'sogou.weixin_gzhcb',
        'type': 1,
    }
    weixin_client.headers['Cookie'] = sg_cookie
    response = weixin_client.request("GET", ARTICLE_LIST_API,
                                     params=params,
                                     format_json=True)
    json_items = response['items']
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
        log.info('some items on the page already exists in db; '
                 'no need to go to next page')
        go_next = False

    article_items = [article_item for url, article_item in item_dict.items()
                     if url not in existed]
    if article_items:
        for article_item in article_items:
            get_article(article_item, gk_user, sg_cookie)

    page += 1
    if total_pages < page:
        log.info('current page is the last page; will not go next page')
        go_next = False

    if go_next:
        log.info('prepare to get next page: %d', page)
        fetch_article_list.delay(gk_user=gk_user, open_id=open_id, ext=ext,
                                 sg_cookie=sg_cookie)


def get_article(article_item, gk_user, sg_cookie):
    cover = article_item.imglink.string
    article_data = dict()
    if cover:
        article_data = {'cover': cover}
    article_link = article_item.url.string
    crawl_article.delay(article_link, gk_user, article_data, sg_cookie)


@task(base=RequestsTask, name='sogou.crawl_article', rate_limit='1/m')
def crawl_article(article_link, gk_user, article_data, sg_cookie):
    weixin_client.headers['Cookie'] = sg_cookie
    url = urljoin('http://weixin.sogou.com/', article_link)
    html_source = weixin_client.request('GET', url=url)
    article_soup = BeautifulSoup(html_source.decode('utf8'))
    # todo: no need to send whole html to task; parse qr_code url first
    if not gk_user['weixin_qrcode_img']:
        get_qr_code.delay(gk_user, parse_qr_code_url(article_soup))

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
    log.info('Insert article. %s', article_info['title'])
    article = Article(**article_info)
    article.save()
    log.info('Insert article. succeed')
    parse_article_content.delay(article.pk)


@task(base=RequestsTask, name='sogou.parse_article_content')
def parse_article_content(article_id):
    article = Article.objects.get(pk=article_id)
    content = article.content
    cover = article.cover
    if cover:
        cover = fetch_image(cover)
        if cover:
            article.cover = cover
            article.save()

    article_soup = BeautifulSoup(content)
    image_tags = article_soup.find_all('img')
    if image_tags:
        for i, image_tag in enumerate(image_tags):
            img_src = (
                image_tag.attrs.get('src') or image_tag.attrs.get('data-src')
            )
            if img_src:
                log.info('fetch_image for article %d: %s', article_id, img_src)
                gk_img_rc = fetch_image(img_src)
                if gk_img_rc:
                    image_tag['src'] = gk_img_rc
                    image_tag['data-src'] = gk_img_rc
                    if not cover and i == 0:
                        article.cover = gk_img_rc
            content_html = article_soup.decode_contents(formatter="html")
            article.content = content_html
            article.save()


def get_token(weixin_id):
    log.info('get open_id for %s', weixin_id)
    open_id = None
    ext = None
    params = dict(type='1', ie='utf8', query=weixin_id)
    weixin_client.refresh_cookies()
    response = weixin_client.request('GET',
                                     url=SEARCH_API,
                                     params=params,
                                     format_json=True)
    sg_cookie = weixin_client.headers.get('Cookie', '')
    for item in response['items']:
        item_xml = clean_xml(item)
        item_xml = BeautifulSoup(item_xml, 'xml')
        if item_xml.weixinhao.string == weixin_id:
            open_id = item_xml.id.string
            ext = item_xml.ext.string
            break

    if open_id:
        return open_id, ext, sg_cookie
    else:
        log.warning('cannot find open_id for weixin_id: %s.', weixin_id)
        return None, None, None


def fetch_image(image_url):
    # log.info('original image url: %s; fixing..', image_url)
    # image_url = fix_image_url(image_url)
    # log.info('fixed image url: %s', image_url)
    # image_name = ''
    log.info('fetch_image %s', image_url)
    if not image_url:
        log.info('empty image url; skip')
        return
    if not image_url.find('mmbiz.qpic.cn') >= 0:
        log.info('image url is not from mmbiz.qpic.cn; skip: %s', image_url)
        return
    from apps.core.utils.image import HandleImage
    r = weixin_client.get(url=image_url, stream=True)
    try:
        try:
            content_type = r.headers['Content-Type']
        except KeyError:
            content_type = 'image/jpeg'
        image = HandleImage(r.raw)
        image_name = image.save()
        # image_full_name = "%s%s" % (image_host, image_name)
        Media.objects.create(
            file_path=image_name,
            content_type=content_type)
        return '/'+image_name

    except (AttributeError, WandException) as e:
        log.error('handle image(%s) Error: %s', image_url, e.message)


def parse_qr_code_url(article_soup):
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
    return 'http://mp.weixin.qq.com/mp/qrcode?scene=%s&__biz=%s' % (scene, biz)


@task(base=RequestsTask, name='sogou.get_qr_code', rate_limit='1/m')
def get_qr_code(gk_user, qr_code_url):
    qr_code_image = fetch_image(qr_code_url)
    gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
    gk_user_instance.weixin_qrcode_img = qr_code_image
    gk_user_instance.save()


def fix_image_url(image_url):
    # todo: is it necessary to fix?
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


if __name__ == '__main__':
    crawl_articles.delay()
