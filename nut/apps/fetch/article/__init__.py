# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import random
from urlparse import urljoin

import redis
import requests
from celery.task import task


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
        except (requests.Timeout, requests.ConnectionError) as e:
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

    def refresh_cookies(self, update=False):
        self.cookies.clear()
        if update:
            update_user_cookie.delay(self.sg_user)

        sg_user = random.choice(
            list(settings.SOGOU_USERS).remove(self.sg_user)
        )
        self._sg_user = sg_user
        sg_cookie = r.get('sogou.cookie.%s' % sg_user)
        self.headers['Cookie'] = sg_cookie
        self.headers['User-Agent'] = faker.user_agent()
        yield self.headers['Cookie']

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


#############  Cookies  #############
sogou_cookies = {'ABTEST=0|1453961496|v1; SNUID=636C782CF6F2DDA83D732912F7C0D636; IPLOC=CN1100; SUID=949B8EDB6B20900A0000000056A9B118; SUID=949B8EDB2E08990A0000000056A9B118; SUV=1453961497207591; ppinf=5|1453961515|1455171115|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxNTE1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=XxCHzbjknPHqqjaBEa70YecLh9XxPvDhlFyh3y6WsWgzmefSEVNM9rzDfN_E48hVbS24eOpmT2Efoxnfb2QDzIrTRVXqkyxg8zOVB_fIWdwlQ5Gv7GTroV1lXkFcbt-kqE_zO2vwEVdjAbtxjNki07siuwYwWoKRXqHH-lILZ9k; CXID=1426F19633322F5F2F45EC265EDEF2C8; ad=3DiNrZllll2Q$b97lllllVzI7vDlllllLcfbOlllll6lllll44Dll5@@@@@@@@@@; sct=1; ppmdig=14539615360000001fbfbc94bd3167ea8362961fc456d8b1'
                 : 'Waser1959@gustr.com',

                 'ABTEST=0|1453961583|v1; SNUID=C9C6D2865D58770292E77C405D80DE9C; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A9B16F; SUID=949B8EDB2E08990A0000000056A9B170; SUV=1453961584721850; CXID=1FDDDEDD36BB0F3FB260FF630435BA03; ppinf=5|1453961598|1455171198|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxNTk4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=ejyv3LwsiLy4UZa_9t0BYCNOL9b1khmx2ODSyFznuTvO5YZrxeY-aoyeunM7PAsnuUWU9cLhHEUyRMqHQdpJWCxI-94HA7caH39nAD47B8ErvObVP0j2dci_iSmF9ZswwG46wASrIPpgRnSXe6e-5SPB0FmLAqbccu6HPxqmIaY; ppmdig=145396160100000001e9fa6b55fbcbf5805e836967acaef8; ad=fcEN@lllll2Q$bV1lllllVzI7YGlllllLcfbOllllxGlllll44Dll5@@@@@@@@@@'
                 : 'asortafairytale@fleckens.hu',

                 'ABTEST=0|1453961654|v1; SNUID=2A253164BEBB94E06C48C014BF8730FA; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A9B1B6; SUID=949B8EDB2E08990A0000000056A9B1B7; SUV=1453961655766748; ppinf=5|1453961669|1455171269|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxNjY5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=mqiVC_RBOZmSPPLnGhlavlJZh1V52_cRnA8RkCpS5ldeoiNj46mXXBDrhnyrEosU4Wgz5ZzLpWpNwU3B1WT5qcjAH0oizMHGtt3bVHzBq5ig3gNPqQKL70JC1-Lmfc0kaicXfywRZvF2GI7F6nQOItrmhbN5hiSDSRfrP0C9ozI; CXID=70634482393A643892E2A1F0BC499DF8; ad=37iNrZllll2Q$b4plllllVzI7tklllllLcfbOlllll6lllll44Dll5@@@@@@@@@@; ppmdig=14539616740000008c81c4566f472ce33300f6b335d093a7; sct=1'
                 : 'Adisaid@jourrapide.com',

                 'ppinf=5|1453961776|1455171376|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxNzc2fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzYW55dWFubWlsa0BmbGVja2Vucy5odXx1bmlxbmFtZTowOnw; pprdig=oUzDmOfftdSB0Zl9dBwShkpVZ3G5spuW64bL5m1mCqTYbaoFkVekLV9v3bk0bhsHXu1-kPcslv0SE2ORYcFjdYIKrQrbPDc-XX-Y2tV04l4tt5_oJEeeJtLW8vJ2wuH6Ps-NaI-fgLvoY2Sc2LMMDXaDXNejlmrbYAkYAN426CQ; IPLOC=CN1100; SUV=0096744BDB8E9B9456A9B23064967398; SUID=949B8EDB2A10950A0000000056A9B230; CXID=8F31E5A7BD1749AA3D790CE47ADA83B7; ad=9bfdrkllll2Q$bwelllllVzI70GlllllLcfbOlllll6lllll44Dll5@@@@@@@@@@; ABTEST=3|1453961781|v1; SNUID=BEB0A4F02A2F0175F0AECC6A2BC253C1; ppmdig=1453961781000000648cf3a285cec4033302fa7e90baf4a1'
                 :'sanyuanmilk@fleckens.hu',

                 'ABTEST=2|1453961873|v1; SNUID=969A8CDA0107285CE1FCCE01022CA7EB; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A9B291; SUID=949B8EDB2E08990A0000000056A9B292; SUV=1453961874264898; CXID=DCB3A3EBC5B0CA3F91D22220DEFF1E81; ppinf=5|1453961885|1455171485|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxODg1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=aUhGwD4acg60jU6hMMPZCz6p3AqC0VqWafM5kC-IGteFvvrqEs4nFTBopSH8QlSrIu_-ja2TrP0CNWZLLLz09e2bxKYM5WwHtVR1mb7CBS5emLkzVSefU2000-0-u5ueJ19n9NPYC2hjXkrQOM30Gj8eoilAPQ-xWkRD-WtNbTs; ad=m2EddZllll2Q$b3qlllllVzI7$llllllLcfbOllllxwlllll44Dll5@@@@@@@@@@; ppmdig=14539618970000005728e96fa0ca00bd8eb05227dd0cb0a1'
                 : 'Andurn@fleckens.hu',

                 'ABTEST=8|1453961953|v1; SNUID=969A8FD90207285CE4C2C1DC02159FD0; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A9B2E1; SUID=949B8EDB2E08990A0000000056A9B2E2; SUV=1453961954368875; ppinf=5|1453961962|1455171562|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYxOTYyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTpyYXRoZTE5ODFAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA; pprdig=NPUTPuN35-JC529J6J_sRXCvMlr7EchXed8WSqkkbo5RUssUgvQ9I58gXA0Ees19ZFcHbTyWW3GKkw1RKyunn6UPt7mVhBLP94QBHUT72Tn0kblWUyifnfAGzANA6z0yzEWAVVEdHdQZ7Y2JjA9m77YwSImhS80R9bRnWQcubho; CXID=97BD4B428A724D752F187629B859E901; ppmdig=1453961965000000cc0dd38b4403818d33ee1274cc27ad79; ad=REfdrkllll2Q$barlllllVzI7mclllllLcfbOlllllklllll44Dll5@@@@@@@@@@'
                 : 'Rathe1981@rhyta.com',

                 'ppinf=5|1453962102|1455171702|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYyMTAyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjp5dW5kYWV4cHJlc3NAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA; pprdig=dbzN9YAPiEAlYaXWkDn0LWYvuAPHZNeNGnvTpI7WHV71-kJbzie7TVO-exoarNwwSGAmntiKB_Wggwexk6As5c8_TyxnH5STWNqUyEyyRUQIDBZ8vMlzbEiowhIMgfu08MzI4wTr9o1ndwMA8DMFJX7w_d4ApiB_nfSv5YzkIMs; IPLOC=CN1100; SUV=0034744DDB8E9B9456A9B37644B1B155; SUID=949B8EDB2A10950A0000000056A9B376; CXID=82ED9FEEC6244721D2062CFF210D6D55; ABTEST=5|1453962105|v1; SNUID=48405200DCD9F185320C4E47DCCAAC25; ad=liid@yllll2Q$b2TlllllVzI7TolllllLcfbOlllll6lllll44Dll5@@@@@@@@@@; ppmdig=145396210900000039af64257efd53a8ea36722f8dcb2871'
                 : 'yundaexpress@rhyta.com',

                 'ABTEST=2|1453962153|v1; SNUID=2434216BAFB59AEE41171CB0B0F59789; IPLOC=CN1100; SUID=949B8EDBE518920A0000000056A9B3A9; SUID=949B8EDB2E08990A0000000056A9B3A9; SUV=1453962153882901; CXID=0523114463899E9863BE9FADB9095987; ppinf=5|1453962171|1455171771|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYyMTcxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDozNTpzdW5zdGFyb3JhYnJlYXRoZmluZUBqb3VycmFwaWRlLmNvbXx1bmlxbmFtZTowOnw; pprdig=tjKnACzlpXoft9W65iEJQl7Vpd7Bkf9PSeGui2jNhZGVysiTgDrpcuod7LTdIW5Pk76PedwF05pccBTfcO_eaQ5HuNuZfHry3KzrHAbKq2SB-PgmOqbzQrgwY-gydaPLFvdVVESMR7fgLTh5i4FkYYvbcnX01VBF13_N1u1jpfo; ppmdig=1453962174000000a44c67fb962a9edc8b130827f63072b5; ad=jafdrkllll2Q$bnslllllVzI7EclllllLcfbOllllx7lllll44Dll5@@@@@@@@@@'
                 : 'sunstarorabreathfine@jourrapide.com',

                 'ppinf=5|1453962213|1455171813|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYyMjEzfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDozMDppbmRvbmVzaWFtYW5kaGVsaW5nQGVpbnJvdC5jb218dW5pcW5hbWU6MDp8; pprdig=dLcvoyEaqm4yutizacqpA9ZzaZQI9pWs4T6bsn-9MDwJoHdmhwHntzkT5_PSWJaBNxKzI8epDxrne-uU-kJZ0BOooqnQ1xlCinddIVW3gALOyHZeQdDU-9uEv0B25y1DVoJHtvajVGosabERPxrrXKbB3gTTZpNHNfqF8DGQ2M4; IPLOC=CN1100; SUV=0043744ADB8E9B9456A9B3E695582857; SUID=949B8EDB2A10950A0000000056A9B3E6; CXID=25654791493ABECA1537626C5FCAAE37; ABTEST=0|1453962215|v1; SNUID=EAE4F0A47E7B54208A1CFE5F7FC250B8; ppmdig=14539622150000000c06a21cca4c2e5be25a3e9add0336eb; ad=Brfd@kllll2Q$b5XlllllVzI7MolllllLcfbOlllll6lllll44Dll5@@@@@@@@@@'
                 : 'indonesiamandheling@einrot.com',

                 'ppinf=5|1453962257|1455171857|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzOTYyMjU3fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDozMjpjaGFybG90dGV3YWxrZm9yc2hhbWVAZGF5cmVwLmNvbXx1bmlxbmFtZTowOnw; pprdig=N4vrDUKYrJs5IUYZkbkWWjn2HNVRJj8KUtlNlZ-JpeeVKSRbBQJRjUdwKNEpzt-wouErA0r2bwE0y9JtPSehIx1Flg_5PLmL9rAgbPOdOoXiKtqgxZV42_y_Mz5m6YKqgAJgbntlpV0GHIRtHSXuBrOWfmUYLgExgW6Wpjl9gyY; IPLOC=CN1100; SUV=0096744BDB8E9B9456A9B41167BE4389; CXID=1682C233D539BAFFD59DE19EBEB4845B; ad=s4i5xkllll2Q$byvlllllVzIHxylllllLcfbOlllllklllll44Dll5@@@@@@@@@@; ABTEST=7|1453962262|v1; SNUID=0F0115409B9FB0C463BEDD7C9BD3B8C9; ppmdig=1453962262000000b91c0f0c9f99f894cc9522ebc9e685ea; SUID=BEB1FD3C2E08990A0000000056A63EB1'
                 : 'charlottewalkforshame@dayrep.com',
                 }


sogou_referers = ('http://weixin.sogou.com/',
                  'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
                  'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
                  )


@task(base=RequestsTask, name="sogou.update_user_cookie")
def update_user_cookie(sg_user):
    if not sg_user:
        return
    get_url = urljoin(settings.PHANTOM_SERVER, '_sg_cookie')
    resp = requests.post(get_url, data={'email': sg_user})
    cookie = resp.json()['sg_cookie']
    key = 'sogou.cookie.%s' % sg_user
    r.set(key, cookie)
