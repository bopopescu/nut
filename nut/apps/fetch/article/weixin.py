#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import random

from django.core.exceptions import MultipleObjectsReturned


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

from wand.exceptions import WandException
from django.conf import settings
from urlparse import urljoin
from celery.task import task
from django.utils.log import getLogger
from datetime import datetime
from bs4 import BeautifulSoup

from apps.core.models import Article, Media, Authorized_User_Profile, GKUser
from apps.fetch.common import clean_xml, queryset_iterator, clean_title
from apps.fetch.article import RequestsTask, WeiXinClient, ToManyRequests, \
    Expired


SEARCH_API = 'http://weixin.sogou.com/weixinjs'
ARTICLE_LIST_API = 'http://weixin.sogou.com/gzhjs'
log = getLogger('django')
weixin_client = WeiXinClient()
qr_code_patterns = (re.compile('biz\s*=\s*"(?P<qr_url>[^"]*)'),
                    re.compile('fakeid\s*=\s*"(?P<qr_url>[^"]*)'),
                    re.compile('appuin\s*=\s*"(?P<qr_url>[^"]*)'))
image_host = getattr(settings, 'IMAGE_HOST', None)


@task(base=RequestsTask, name='sogou.crawl_articles')
def crawl_articles():
    all_authorized_user = Authorized_User_Profile.objects.filter(
        weixin_id__isnull=False
    )
    for user in queryset_iterator(all_authorized_user):
        gk_user = {
            'weixin_openid': user.weixin_openid,
            'weixin_id': user.weixin_id,
            'pk': user.pk,
            'weixin_qrcode_img': user.weixin_qrcode_img,
            'gk_user_pk': user.user.pk
        }
        fetch_article_list.delay(gk_user)


@task(base=RequestsTask, name='sogou.fetch_article_list')
def fetch_article_list(gk_user, page=1):
    open_id, ext, sg_cookie = get_tokens(gk_user['weixin_id'])
    if not open_id:
        log.warning("skip user %s: cannot find open_id. Is weixin_id correct?",
                    gk_user['weixin_id'])
        return
    if not gk_user.get('weixin_openid'):
        # save open_id if it's not set already
        gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
        gk_user_instance.weixin_openid = open_id
        gk_user_instance.save()
        gk_user['weixin_openid'] = open_id

    go_next = True
    jsonp_callback = 'sogou.weixin_gzhcb'
    params = {
        'openid': open_id,
        'ext': ext,
        'page': page,
        'cb': jsonp_callback,
        'type': 1,
    }
    response = weixin_client.get(ARTICLE_LIST_API,
                                 params=params,
                                 jsonp_callback=jsonp_callback,
                                 headers={'Cookie': sg_cookie})

    item_dict = {}
    for article_item in response.jsonp['items']:
        article_item_xml = clean_xml(article_item)
        article_item_xml = BeautifulSoup(article_item_xml, 'xml')
        title = clean_title(article_item_xml.title1.text)
        item_dict[title] = article_item_xml

    existed = []
    for item in item_dict.keys():
        article = Article.objects.values_list(
            "title"
        ).filter(
            cleaned_title__startswith=item,
            creator=gk_user['gk_user_pk']
        )
        if article:
            existed.append(item)

    if existed:
        log.info('some items on the page already exists in db; '
                 'no need to go to next page')
        go_next = False

    item_dict = {key: value for key, value
                 in item_dict.items() if key not in existed}
    for article_item in item_dict.values():
        crawl_article.delay(
            article_link=article_item.url.string,
            gk_user=gk_user,
            article_data=dict(cover=article_item.imglink.string),
            sg_cookie=sg_cookie,
            page=page,
        )

    page += 1
    if int(response.jsonp['totalPages']) < page:
        log.info('current page is the last page; will not go next page')
        go_next = False

    if go_next:
        log.info('prepare to get next page: %d', page)
        fetch_article_list.delay(gk_user=gk_user, page=page)


@task(base=RequestsTask, name='sogou.crawl_article')
def crawl_article(article_link, gk_user, article_data, sg_cookie, page):
    url = urljoin('http://weixin.sogou.com/', article_link)
    try:
        resp = weixin_client.get(
            url=url, headers={'Cookie': sg_cookie})
    except (ToManyRequests, Expired) as e:
        # if too frequent error, re-crawl the page the current article is on
        log.warning("too many requests or request expired. %s", e.message)
        fetch_article_list.delay(gk_user=gk_user, page=page)
        return

    article_soup = BeautifulSoup(resp.utf8_content, from_encoding='utf8')
    if not gk_user['weixin_qrcode_img']:
        get_qr_code.delay(gk_user, parse_qr_code_url(article_soup))

    title = article_soup.select('h2.rich_media_title')[0].text
    published_time = article_soup.select('em#post-date')[0].text
    published_time = datetime.strptime(published_time, '%Y-%m-%d')
    content = article_soup.find('div', id='js_content')
    creator = GKUser.objects.get(pk=gk_user['gk_user_pk'])

    try:
        article, created = Article.objects.get_or_create(
            title=title,
            creator=creator,
        )
    except MultipleObjectsReturned as e:
        log.error("duplicate articles, title: %s."
                  " will use the first one. %s", title, e.message)
        article = Article.objects.filter(
            title=title,
            creator=creator,
        ).first()
        created = False

    if created:
        article_info = dict(
            content=content.decode_contents(formatter="html"),
            created_datetime=published_time,
            publish=Article.published,
        )
        article_info.update(article_data)
        article.update(**article_info)
        article.save()
        log.info('insert article. %s', article_info['title'])

    cover = fetch_image(article.cover)
    if cover:
        article.cover = cover
        article.save()

    article_soup = BeautifulSoup(article.content)
    image_tags = article_soup.find_all('img')
    if image_tags:
        for i, image_tag in enumerate(image_tags):
            img_src = (
                image_tag.attrs.get('src') or image_tag.attrs.get('data-src')
            )
            if img_src:
                log.info('fetch_image for article %d: %s', article.id, img_src)
                gk_img_rc = fetch_image(img_src)
                if gk_img_rc:
                    image_tag['src'] = gk_img_rc
                    image_tag['data-src'] = gk_img_rc
                    if not cover and not article.cover and i == 0:
                        article.cover = gk_img_rc
            content_html = article_soup.decode_contents(formatter="html")
            article.content = content_html
            article.save()


def get_tokens(weixin_id):
    log.info('get open_id for %s', weixin_id)
    open_id = None
    ext = None
    params = dict(type='1', ie='utf8', query=weixin_id)
    weixin_client.refresh_cookies()
    response = weixin_client.get(url=SEARCH_API,
                                 params=params,
                                 jsonp_callback='weixin',
                                 headers={'Cookie':weixin_client.headers.get('Cookie')})
    sg_cookie = weixin_client.headers.get('Cookie')
    for item in response.jsonp['items']:
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


@task(base=RequestsTask, name='sogou.get_qr_code')
def get_qr_code(gk_user, qr_code_url):
    qr_code_image = fetch_image(qr_code_url)
    gk_user_instance = Authorized_User_Profile.objects.get(pk=gk_user['pk'])
    gk_user_instance.weixin_qrcode_img = qr_code_image
    gk_user_instance.save()


if __name__ == '__main__':
    crawl_articles.delay()
