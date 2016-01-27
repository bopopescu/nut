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
sogou_cookies = {'IPLOC=CN1100; SUV=0043744ADB8E9B9456A86293DC41C973; CXID=7956AB51C464DEAB8114F1C3E3D7B85B; ppinf=5|1453875872|1455085472|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzODc1ODcyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=kh1oGpL3D2EqWz_NILr6Pz7cfb-lyQ81hLRso4g7lI1h54ddP0rKV90r1iHYIMqjY-oSBF15wszUeRTO11MaRLhbiyfJhXPt-RaaPXzrUgmxxLRjpDIeIEyJ2ut8Q19dhyvYjJJDxtItlmKI6YCxO42TkAhKl2llLuurdzzgJhs; ad=KfcNVkllll2Q$p3UlllllVzoY$GlllllLcfbOllllx9lllllpTDll5@@@@@@@@@@; ABTEST=0|1453875877|v1; SNUID=353B2E7BA0A48AEB7A934FA7A1D8850D; ppmdig=14538758770000002954fc13cf4c2867d4dff5f816d95ad6; SUID=BEB1FD3C2E08990A0000000056A63EB1':'Waser1959@gustr.com',
                 'IPLOC=CN1100; SUV=0034744DDB8E9B9456A862186B42E890; SUID=949B8EDB2A10950A0000000056A86218; CXID=D2E2B5725C91C9D6EB51D13A073F1689; ppinf=5|1453875745|1455085345|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzODc1NzQ1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=YY1xFpK0zHlsIuGXeE1NAlnRe1crMoZy8C2h9xJb9CaC8Z14RkCPbxG-Qu7tu7b3xsk9NLhpaZXQOaHpDIxYy7WlDcqkzoKZ9CoxRNQIKsP9sgx4CcRaKjkMp6pkYeYucoElZXLOiLlgNEiTQQzSAO5lq5aMjr-isHNfCV9r6Mg; ad=tzcNVkllll2Q$pwBlllllVzoYAGlllllLcfbOlllll7lllllpTDll5@@@@@@@@@@; ABTEST=7|1453875747|v1; ppmdig=1453875747000000494b5d2e51ed1e9eadc40022e5ef2c6f; weixinIndexVisited=1; SNUID=444B5E0AD0D4FA9A0373D271D1351465':'asortafairytale@fleckens.hu',
                 'ABTEST=0|1453735601|v1; SUID=BEB1FD3C6F1C920A0000000056A63EB1; SUV=1453735601789275; SUIR=3A3578B98581AEAEB79893BD859538F0; IPLOC=CN1100; weixinIndexVisited=1; CXID=F50B4A3F321A508EBBC54EFC39B6660F; sct=1; SNUID=19165B9AA7A38DE6AD64AEA5A7E6CA1A; SUID=BEB1FD3C2E08990A0000000056A63EB1; ppinf=5|1453875643|1455085243|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzODc1NjQzfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=kGmj9MdvJF9prYRyYacvVqnBsCTsXBQxKtmL-3oHFCdCygOJBSnPJi8_JyIoB-nhwGrXZTAXTC9F2aVqD1FNMz4XHsn_oDELOuuEl8Cmgmqic3BnxIflhvoXZGBLMup9g_RMvSEpgUw0dH2-nwl96rp7jqISOIOxCHahSTVoNB8; ppmdig=145387564600000038bbf74e0273228924f6b6a9cb676e38; ad=m2fOJyllll2QIfsJlllllVzoYbclllll55LeskllllclllllpTDll5@@@@@@@@@@; LSTMV=260%2C351; LCLKINT=1441':'Adisaid@jourrapide.com',
                 'SUV=00636E6CDB8E9B9456A850A0AF333674; ppinf=5|1453871269|1455080869|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxMjY5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzYW55dWFubWlsa0BmbGVja2Vucy5odXx1bmlxbmFtZTowOnw; pprdig=ZcJJbYily2_RTz0mWfBSfR86u3PH-TMqnsd7FzWyTjB685B-SX_99aRIqVbJxrpm5L4SnNP8h4a1pMtZGDZ6FFyGBT6jpu8i2NAhrWji7zbkmQQ60k3etCfAKlIK30mP5v78G5Q5so3FrMQHsLGmWreSM5MsQ_yFPrO_BJJJXAk; ABTEST=6|1453871277|v1; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A850AD; SUID=949B8EDB2E08990A0000000056A850AE; weixinIndexVisited=1; SNUID=E0EEFAAF74705F3CBDC4FB99750A4758':'sanyuanmilk@fleckens.hu',
                 'IPLOC=CN1100; SUID=949B8EDB2E08990A0000000056A8511B; SUV=1453871387428707; ppinf=5|1453871418|1455081018|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxNDE4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=ZbeT3cKkp6lR9xAa35Ite4YKhGT5twPL3emCF_ejWzM8zOLT-WKUlM8zCm1UpOrRxlrcPduzW8vo2iJOwGToDtyslEtopuNuqtyltbpAB5luUsXmZb5NcBO0tH9jFD-qZF265iJpD5n9mEqCSTrqG3eMOpbFmo2exZLaYB3uHX4; ABTEST=6|1453871429|v1; weixinIndexVisited=1; sct=1; SNUID=8A8491C51E1A3457CC455A961FA564B2':'Andurn@fleckens.hu',
                 'SUV=006B79BADB8E9B9456A85193AAB40493; ppinf=5|1453871515|1455081115|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDUzODcxNTE1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTpyYXRoZTE5ODFAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA; pprdig=mVxtzXRhjw1JKX8rJ6NgmaHx3rvTV9zRmivDbvx3iVObQoYX0MQNJfi5he--17JwgJuD5lkAridvkJnLJpIVLqJrccTHcMDN1hxR9Xebugv5CN2px8QZuqOeG-wa7169mV3Yjjoiq2GaN2DrVjfRzfc6tjM4eYvTUDSUThySeZ8; ABTEST=0|1453871519|v1; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A8519F; SUID=949B8EDB2E08990A0000000056A8519F; weixinIndexVisited=1; sct=1; SNUID=15190F598284A8C8553499FF82C25AF0':'Rathe1981@rhyta.com',

                 }


sogou_referers = ('http://weixin.sogou.com/',
                  'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
                  'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
                  )
