# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from time import sleep

import requests

from faker import Faker
from celery import Task
from django.conf import settings
from django.utils.log import getLogger
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


faker = Faker()
search_api = 'http://weixin.sogou.com/weixinjs'
login_url = 'https://account.sogou.com/web/login'
log = getLogger('django')


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
        except (requests.Timeout, requests.ConnectionError) as e:
            raise self.retry(exc=e)


class WeiXinClient(requests.Session):
    def __init__(self):
        super(WeiXinClient, self).__init__()
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

        cookie_user = sogou_cookies.get(self.headers['Cookie'])
        resp.utf8_content = resp.content.decode('utf-8')
        resp.utf8_content = resp.utf8_content.rstrip('\n')
        if resp.utf8_content.find(u'您的访问过于频繁') >= 0:
            log.warning(u'访问的过于频繁. 用户: %s, url: %s', cookie_user, url)
            raise ToManyRequests(message=u'too many requests.')
        if resp.utf8_content.find(u'当前请求已过期') >= 0:
            log.warning(u'当前请求已过期. url: %s', url)
            raise Expired('link expired: %s' % url)
        if jsonp_callback:
            resp.jsonp = self.parse_jsonp(resp.utf8_content, jsonp_callback)
            if resp.jsonp.get('code') == 'needlogin':
                self.refresh_cookies()
                raise Retry(message=u'need login.')
        sleep(60)
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

    def refresh_cookies(self):
        self.cookies.clear()
        self.headers['Cookie'] = random.choice(sogou_cookies.keys())
        self.headers['User-Agent'] = faker.user_agent()
        return self.headers['Cookie']

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


#############  Cookies  #############
sogou_cookies = {'SUV=00BA2EFF7C7F461156CBD1AB80A39532; ppinf=5|1456198079|1457407679|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU2MTk4MDc5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=khGQbi5UJjWX8_LMLPFvHF-_wqdiL7NtgjZju-t6B6HMI5FJ-bb_Ht3IXc50RvF2wVbzrS-oM1UBydKLOmC3Kmu9oSebPoUAUchjCTl0SW8BFJwd72BiH7_PPLVq_WOKYwYb127linLQZyFUKKuvIOj3XjO0uJge__r4GYcFjD4; ABTEST=0|1456198084|v1; SNUID=0651676417123B7F9E884CF0184E31B0; ppmdig=14561980840000003233ce960d11336bd5f1c9d559a21d19; IPLOC=CN1100; SUID=11467F7C6A20900A0000000056CBD1C4; SUID=11467F7C2524920A0000000056CBD1C5'
                 : 'waser1959@gustr.com',

                 'SUV=004A5FA17C7F461156CBD1F4462F6572; ppinf=5|1456198135|1457407735|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU2MTk4MTM1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=m7lGKvD0md9FbYdtKwBzbt-E1pKRkyvByq0-AVlPyNX5af572RIfW7Qmz7AyR4f4QnZNayI0kdY_8ZngCbGv4Sn3Ps8MV3RhRetP5oe9qCOvH_eDeXG1xSF_mHV0OSw-V_XduM5zFYcZ5pGHvWwm3_3F3EQgLk-YHI0UUgI17VM; ABTEST=8|1456198138|v1; SNUID=DD8AB3B1CDC8E0AB41099250CD911C01; ppmdig=1456198138000000401b35367b6b1f421b8d9ea4daa0d98c; IPLOC=CN1100; SUID=11467F7C6A20900A0000000056CBD1FA; SUID=11467F7C2524920A0000000056CBD1FB'
                 : 'asortafairytale@fleckens.hu',

                 'SUV=001F681F7C7F461156CBD22DCD3A2818; ppinf=5|1456198192|1457407792|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU2MTk4MTkyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=itPm5BZ5cBo0Ys0pcY6_WbDr7mEsk3cc0ITMWq6BjB19RDDkFCHmOoUxjFxtM6CXpZd52RcuGtdCvydAyujaTq1H7UY-LoYp-S4atxuVdnzXaJef8iBeEKAM31pFPGMHkGsJNTC1z2jfVKWq6sa-1aTs-HMZjxtvhI5L49L0lAM; ABTEST=0|1456198195|v1; SNUID=B7E0D9DAA6A08AC13681A440A6CEFBA1; ppmdig=145619819500000077ddb9875627c0425efa7343200b01ef; IPLOC=CN1100; SUID=11467F7C6A20900A0000000056CBD233; SUID=11467F7C2524920A0000000056CBD234'
                 : 'adisaid@jourrapide.com',

                 'SUV=00835FA07C7F461156CBD25CD5B5B304; ppinf=5|1456198240|1457407840|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU2MTk4MjQwfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTpyYXRoZTE5ODFAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA; pprdig=WzP6FouKIZa-0hcwGqPIOnqFl3Zjst-Lvucd9pA2tA1CPBywtciUl3Z5K41eSB7Z1nrjagOsQ2CC6FJIhHSwZjsggKpUL5PX29L5k3S4AAxE3QIRn8uBCDNrWWaIhG08n0Te3aN17DLnbFjY7ZfHSMw7Wu_mctmI4B_HeKhmf8c; ABTEST=0|1456198243|v1; SNUID=ADFDC4C7BCBE97DC28B1DA7FBC338849; ppmdig=14561982430000007b4d72dd5a3d465e40185782dea5e30a; IPLOC=CN1100; SUID=11467F7C6A20900A0000000056CBD263; SUID=11467F7C2524920A0000000056CBD264'
                 : 'rathe1981@rhyta.com'
                 }


sogou_referers = ('http://weixin.sogou.com/',
                  'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
                  'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
                  )

# @task(base=RequestsTask, name="sogou.update_user_cookie")
# def update_user_cookie(sg_user):
#     if not sg_user:
#         return
#     get_url = urljoin(settings.PHANTOM_SERVER, '_sg_cookie')
#     resp = requests.post(get_url, data={'email': sg_user})
#     cookie = resp.json()['sg_cookie']
#     key = 'sogou.cookie.%s' % sg_user
#     r.set(key, cookie)
