# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import random
import requests


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev_judy'

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
    pass


class ToManyRequests(Exception):
    pass


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
            raise ToManyRequests(message=u'访问的过于频繁.')
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
sogou_cookies = {
                 # 'ABTEST=0|1453548274|v1; weixinIndexVisited=1; ppinf=5|1453551361|1454760961|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTUxMzYxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=JUy6ve-X1fdWDQWGEMH9jMV448YiF-NHG5dm3MTSPNmJasMDtuvfo5rgYQIEpTUqmfY3jghcimxj6zxC9sqt5KOf3r-6uT3lfkBCa_z6NSYMsW1FkL1wB1WkVmoAeNkp2rMIGKTOLYyuR0T_go2uxP8S_uCq0kNpW0N3AIRu9D0; SUV=008F17DE3CFDB1BE56A36F01F1E13976; SUID=BEB1FD3C3428950A0000000056A36F01; CXID=1F9E4F4E2D3ED2C0479B94D78E6DF27D; ad=xNEdQZllll2QoLDjlllllVz0bZUlllll55Leskllll6lllllVTDll5@@@@@@@@@@; sct=2; PHPSESSID=evqkjrk7sv6h521nd377oanlj3; SUIR=DCD09F5E6167489E2C75BEAB6279B4C7; LSTMV=431%2C256; LCLKINT=1476; IPLOC=EU; CXID=D42B30640BDD38A628347F75EFBB9E5B; SUV=003723E580C7F7D656A70D986485B572; SUID=D6F7C780523A900A0000000056A70D98; ppinf=5|1453788602|1454998202|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNzg4NjAyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=ji90mg8ByUNXzAHoE71mnB-ApnysVzD4uWwG_Xo7rYBfzFXpyE814mdDhYiJRuF1UWvyBv1YC62SL71n3wbRGlcyXHMcoe8CN-ieYGVU9IoaQqrD0uWBOFh2EIa0vufVPHFCJmhItCXlklJtzSTyGRbhXzHv9GwXrweHVoHWLIc; ad=eafdVkllll2QIZLglllllVzXRbclllllkGKTCkllllDlllllpXDll5@@@@@@@@@@; SNUID=79E98D88F4F6DEC568CE713BF4792A96; sct=3; ppmdig=145379222800000094c21b48ddf0b2e0117abaca07ca5e2a; IPLOC=CN1100':'Waser1959@gustr.com',
                 # 'IPLOC=CN1100; SUV=00A315937B791A8A56A71C7895F14815; CXID=7757854367D862007DE377A7D381F88C; ppinf=5|1453792401|1455002001|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNzkyNDAxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=R-XFwnmDi1iP3lGN3HFq2-wn0bkTzGOtolSBclzQsrkWrwdGxCsLmWwoJtig6xax7kMX7U2E0r0tDk2DBi3XgCYHpOc0pq7n98L0h8cuU8a9qlPAPK_BM8dwJ-USb1luYF3MSZHIU2vt_2ke_bFylJ1gGNcc_sVhiE7t6VI6i1g; ad=cHEd4Zllll2QIeeclllllVzX43UlllllWT6zAklllxolllllpXDll5@@@@@@@@@@; ABTEST=0|1453792423|v1; SNUID=40D0B0B2CACFE3FDA63D0628CA90CDC3; ppmdig=145379242300000014dea59a6d656f3bbbd624469da68057; SUID=8A1A797B533A900A0000000056A71C78':'asortafairytale@fleckens.hu',
                 # 'SUV=000A70C87B791A8A56A71CCD90777265; IPLOC=CN1100; SUID=8A1A797B533A900A0000000056A71CCD; CXID=3F0824E3515037BAB2AAEB9569A295FE; ppinf=5|1453792478|1455002078|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNzkyNDc4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=xXmHla9VnIeOV8Wn3hephnCoIdA2y_MOkAEuRLHFwGx0-5IWkVSoGxiAfL6mU0VGY0Uk2dP1Vst7qstqosQVwFdskA32OkEIDAeYoVsJM1xZjOSA2JxVEWTPuBkKn81v8QgJYAP-m4jKfXBFeaBWHBFJGrfHBDJr9Z3B5H_pYlA; ad=v5EQalllll2QIe8nlllllVzX4nwlllllWT6zAklllxGlllllpXDll5@@@@@@@@@@; ABTEST=8|1453792482|v1; SNUID=1282E0E2989DB3AFE818578F995E32FA; ppmdig=14537924820000004b1aec42e9958698eaf1810dd0caac0e':'Adisaid@jourrapide.com',
                 'SUV=00636E6CDB8E9B9456A850A0AF333674; ppinf=5|1453871269|1455080869|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxMjY5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzYW55dWFubWlsa0BmbGVja2Vucy5odXx1bmlxbmFtZTowOnw; pprdig=ZcJJbYily2_RTz0mWfBSfR86u3PH-TMqnsd7FzWyTjB685B-SX_99aRIqVbJxrpm5L4SnNP8h4a1pMtZGDZ6FFyGBT6jpu8i2NAhrWji7zbkmQQ60k3etCfAKlIK30mP5v78G5Q5so3FrMQHsLGmWreSM5MsQ_yFPrO_BJJJXAk; ABTEST=6|1453871277|v1; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A850AD; SUID=949B8EDB2E08990A0000000056A850AE; weixinIndexVisited=1; SNUID=E0EEFAAF74705F3CBDC4FB99750A4758':'sanyuanmilk@fleckens.hu',
                 'IPLOC=CN1100; SUID=949B8EDB2E08990A0000000056A8511B; SUV=1453871387428707; ppinf=5|1453871418|1455081018|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxNDE4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=ZbeT3cKkp6lR9xAa35Ite4YKhGT5twPL3emCF_ejWzM8zOLT-WKUlM8zCm1UpOrRxlrcPduzW8vo2iJOwGToDtyslEtopuNuqtyltbpAB5luUsXmZb5NcBO0tH9jFD-qZF265iJpD5n9mEqCSTrqG3eMOpbFmo2exZLaYB3uHX4; ABTEST=6|1453871429|v1; weixinIndexVisited=1; sct=1; SNUID=8A8491C51E1A3457CC455A961FA564B2':'Andurn@fleckens.hu',
                 'SUV=006B79BADB8E9B9456A85193AAB40493; ppinf=5|1453871515|1455081115|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxNTE1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTpyYXRoZTE5ODFAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA; pprdig=mVxtzXRhjw1JKX8rJ6NgmaHx3rvTV9zRmivDbvx3iVObQoYX0MQNJfi5he--17JwgJuD5lkAridvkJnLJpIVLqJrccTHcMDN1hxR9Xebugv5CN2px8QZuqOeG-wa7169mV3Yjjoiq2GaN2DrVjfRzfc6tjM4eYvTUDSUThySeZ8; ABTEST=0|1453871519|v1; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A8519F; SUID=949B8EDB2E08990A0000000056A8519F; weixinIndexVisited=1; sct=1; SNUID=15190F598284A8C8553499FF82C25AF0':'Rathe1981@rhyta.com',


                 }


sogou_referers = ('http://weixin.sogou.com/',
                  'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
                  'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
                  )
