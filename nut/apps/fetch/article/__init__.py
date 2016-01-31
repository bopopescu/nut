# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import random
import requests

from faker import Faker
from celery import Task
from urlparse import urljoin
from celery.task import task
from django.conf import settings
from django.utils.log import getLogger
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


faker = Faker()
search_api = 'http://weixin.sogou.com/weixinjs'
login_url = 'https://account.sogou.com/web/login'
log = getLogger('django')
r = redis.Redis(host=settings.CONFIG_REDIS_HOST,
                port=settings.CONFIG_REDIS_PORT,
                db=settings.CONFIG_REDIS_DB)


class Retry(Exception):
    def __init__(self, countdown=5, message=u''):
        self.countdown = countdown
        self.message = 'Fetch error, need to login or get new token.' + message


class Expired(Exception):
    def __init__(self, message=u''):
        self.message = message


class ToManyRequests(Exception):
    def __init__(self, message=u''):
        self.message = message


class RequestsTask(Task):
    abstract = True
    compression = 'gzip'
    default_retry_delay = 5
    send_error_emails = True
    max_retries = 3

    def __call__(self, *args, **kwargs):
        try:
            return super(RequestsTask, self).__call__(*args, **kwargs)
        except (requests.Timeout, requests.ConnectionError, Retry) as e:
            raise self.retry(exc=e)


class WeiXinClient(requests.Session):
    def __init__(self):
        super(WeiXinClient, self).__init__()
        self._sg_user = None
        self.login_url = 'https://account.sogou.com/web/login'
        self.search_api_url = 'http://weixin.sogou.com/weixinjs'
        self.refresh_cookies()

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
                jsonp_callback=None):
        try:
            resp = super(WeiXinClient, self).request(method, url, params, data,
                                                     headers, cookies, files, auth,
                                                     timeout, allow_redirects,
                                                     proxies, hooks, stream, verify,
                                                     cert, json)
        except ConnectionError as e:
            raise Retry(message=u'ConnectionError. %s' % e.message)
        except ReadTimeout as e:
            raise Retry(message=u'ReadTimeout. %s' % e.message)
        if stream:
            return resp

        resp.utf8_content = resp.content.decode('utf-8')
        resp.utf8_content = resp.utf8_content.rstrip('\n')
        if resp.utf8_content.find(u'您的访问过于频繁') >= 0:
            log.warning(u'访问的过于频繁. 用户: %s, url: %s', self.sg_user, url)
            raise ToManyRequests(message=u'too many requests.')
        if resp.utf8_content.find(u'当前请求已过期') >= 0:
            log.warning(u'当前请求已过期. url: %s', url)
            raise Expired('link expired: %s' % url)
        if jsonp_callback:
            resp.jsonp = self.parse_jsonp(resp.utf8_content, jsonp_callback)
            if resp.jsonp.get('code') == 'needlogin':
                self.refresh_cookies()
                raise Retry(message=u'need login.')
        return resp

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

    def refresh_cookies(self, update=False):
        self.cookies.clear()
        if update:
            update_user_cookie.delay(self.sg_user)

        sg_users = list(settings.SOGOU_USERS)
        if self.sg_user:
            sg_users.remove(self.sg_user)
        sg_user = random.choice(sg_users)
        self._sg_user = sg_user
        sg_cookie = r.get('sogou.cookie.%s' % sg_user)
        self.headers['Cookie'] = sg_cookie
        self.headers['User-Agent'] = faker.user_agent()

    @property
    def sg_user(self):
        return self._sg_user

    @classmethod
    def parse_jsonp(cls, utf8_content, callback):
        if utf8_content.startswith(callback):
            try:
                # utf8 content is a jsonp
                # here we extract the json part
                # for example, "cb({"a": 1})", where callback is "cb"
                return json.loads(utf8_content[len(callback) + 1:-1])
            except ValueError:
                log.error("Json decode error %s", utf8_content)
                raise


@task(base=RequestsTask, name="sogou.update_user_cookie")
def update_user_cookie(sg_user):
    if not sg_user:
        return
    get_url = urljoin(settings.PHANTOM_SERVER, '_sg_cookie')
    resp = requests.post(get_url, data={'email': sg_user})
    cookie = resp.json()['sg_cookie']
    key = 'sogou.cookie.%s' % sg_user
    r.set(key, cookie)
