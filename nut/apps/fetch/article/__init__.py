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
from django.conf import settings
from django.utils.log import getLogger
from celery import Task
from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


faker = Faker()
search_api = 'http://weixin.sogou.com/weixinjs'
login_url = 'https://account.sogou.com/web/login'
log = getLogger('django')


class Retry(Exception):
    def __init__(self, countdown=5):
        self.countdown = countdown
        self.message = 'Fetch error, need to login or get new token.'


class RequestsTask(Task):
    abstract = True
    compression = 'gzip'
    default_retry_delay = 5
    send_error_emails = True
    max_retries = 3
    rate_limit = '2/m'

    def __call__(self, *args, **kwargs):
        try:
            return super(RequestsTask, self).__call__(*args, **kwargs)
        except (requests.Timeout, requests.ConnectionError) as e:
            raise self.retry(exc=e)
        except Retry as e:
            raise self.retry(countdown=e.countdown)


class WeiXinClient(requests.Session):
    def __init__(self):
        super(WeiXinClient, self).__init__()
        self.login_url = 'https://account.sogou.com/web/login'
        self.search_api_url = 'http://weixin.sogou.com/weixinjs'

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
                format_json=False):
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
        result = resp.content.decode('utf-8')
        result = result.rstrip('\n')
        if result.find(u'您的访问过于频繁') >= 0:
            log.warning(u'访问的过于频繁. url: %s', url)
            self.cookies.clear()
            self.headers['Cookie'] = random.choice(cookies.values)
            self.headers['User-Agent'] = faker.user_agent()
            self.headers['Referer'] = random.choice(referers)
            raise Retry
        if format_json:
            result = self.json_response(resp)
            if 'code' in result and result['code'] == "needlogin":
                self.login()
                raise Retry
        return result

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


#############  Cookies  #############
cookies = {
    'Waser1959@gustr.com': {'ppmdig': '1453397330000000c83c143bec3f757d06144cf1697d4f4a', 'ad': 'vHEdKZllll2QoSqJlllllVzPVU7lllllLcfbOlllll6lllllVgDll5@@@@@@@@@@', 'SUID': '949B8EDB2A10950A0000000056A11548', 'ppinf': '5|1453397320|1454606920|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3MzIwfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA', 'SNUID': '2E213561BBBF9261CAAE5201BB372A72;', 'ABTEST': '0|1453397330|v1', 'CXID': 'CEF4CCEAE4C33B94EBE0CBB26CA8A603', 'SUV': '0043744ADB8E9B9456A115489E542674', 'PHPSESSID': 'u7lmaa86vrl9lesn6c5a6ecgb3', 'SUIR': '1453397330', 'pprdig': 'B3_zIgFj-XJHeEWSYu5UjbBcJtHlcQHQP8z4ZB5eD4ipwngIKggwrl3J9XCYaIANjHpCv9oS28JFBFkOaR4HAXP7Plv4SIBslWnBfkCUk_ZyKzPZwx3oI-SuxGEpXiynpOIZIz-IRcbwhkdbadgjF8KtU4DhrV987raKEOiwc8o', 'IPLOC': 'CN1100'},
    'asortafairytale@fleckens.hu': {'SNUID': '76796F3AE1E4CB3BD751771CE2BCC396', 'ABTEST': '0|1453386418|v1', 'IPLOC': 'CN1100', 'ad': 'sHEdJZllll2Qon@@@@@@@@@@', 'SUID': '949B8EDB2A10950A0000000056A0EAB7', 'pprdig': 'rztHrGmvYAKsxEuSFoku0TqqMXacNMaSZqGxISh4XoT0ELieC6GGLpB7RoawOQvavrTDCxJu6VcsXJ2s8HGKkOXWok1k2nVbC2oaApIhAy0AzHvk2G0zdzBRKpZMJOKA2CBUONZ5q6IWWvtsJBWm3KOIWm2p48MFHlE2wrpTuR4', 'SUIR': '1453387763', 'sct': '9', 'CXID': 'DA3B77DAF66D29E3DEF0A1A773218CD2', 'SUV': '00161002DB8E9B9456A0EA01A7B25989', 'weixinIndexVisited': '1', 'ppinf': '5|1453396731|1454606331|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk2NzMxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8'},
    'Adisaid@jourrapide.com': {'ppinf': '5|1453396873|1454606473|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk2ODczfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA', 'pprdig': 'sWjqVRUbvsuMsnWg65ckxpFh8_JgPDB1-N5iclB3rvuTtC2V-hSyBKXLuAqL-wuYXxNR-BX56OmZLEVs9OjyISfB4di9-Yh33_OV1BfQTDmRGk6CqqOAMKW6EG_H0yOpHxvwfyBBgwMXEM8tMuPEIExT933kKa85yU9l_k_BbtE', 'seccodeRight': 'success', 'ppmdig': '145339674200000047be4ee76732a6aa8db180f0c46ab2d0', 'SNUID': '0F0712479B99B547CE4BE8469C2477E5', 'IPLOC': 'CN1100', 'PHPSESSID': 'bevobnbosau8picf198jcag1u2', 'successCount': '1', 'ad': 'eYENXlllll2QoSn3lllllVzP9i6lllllLcfbOllllxwlllllVgDll5@@@@@@@@@@', 'SUV': '00E0744CDB8E9B9456A1138ABCF2C154', 'weixinIndexVisited': '1', 'ABTEST': '0|1453386418|v1', 'SUID': '949B8EDB2A10950A0000000056A1138A', 'SUIR': '1453396879', 'CXID': '2CEBBC1F1DA02CB2DEAA08803805603F'},
    'Rathe1981@rhyta.com': {'SUIR': '1453397078', 'ppinf': '5|1453397066|1454606666|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3MDY2fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTpyYXRoZTE5ODFAcmh5dGEuY29tfHVuaXFuYW1lOjA6fA', 'SUID': '949B8EDB2A10950A0000000056A11436', 'pprdig': 'i750ZJmx4IQxB4PsekxTvD4hgG91bmY1JfmMjSU_jlfHkRwGjntPZR183ouiPgDpDN0n8TRmZ8PZR0yrUcyWuvqUsA9fcBlWG6P5BTmswEjL4Mux2ezSriM3Wghw8v97PdpHM6vOFmLZtcnz-3ft-GhYZ-gQ2XjEWJGWJRLG2SE', 'seccodeRight': 'success', 'CXID': 'AB66F8187F49EDF50455ED71921AC8B2', 'SUV': '0034744DDB8E9B9456A11436756E7141', 'ppmdig': '145339674200000057f320ac8be269d9502639450dd8264a', 'SNUID': '67687C29F3F7DB29930ED0D0F395C810', 'ABTEST': '0|1453386418|v1', 'IPLOC': 'CN1100', 'ad': 'D@@@@@@@@@@', 'weixinIndexVisited': '1', 'PHPSESSID': 'bevobnbosau8picf198jcag1u2'},
    'Andurn@fleckens.hu': {'ppmdig': '1453396742000000532ba8fcfa8e01b934ba03e2909ddac2', 'ad': 'hIidKyllll2QoSv1lllllVzPVatlllllLcfbOlllllolllllVgDll5@@@@@@@@@@', 'SUIR': '1453397175', 'SUID': '949B8EDB2A10950A0000000056A114B4', 'pprdig': 'w7qeRmbO5xtfoCTOJMpTl_oy8vEytQvDD4rJ41c8DLHhpE8rbMj0kMB4xXZaTkriME9mj-3G0rBGSH3cmaHE45P3WSujz5LWcFx5ariiKsjpCpDr-AlCuBAt9shxDR57_Rhq_skjOztBqAKaUmn1kT5ujPKCzO5AQKyds-koLq4', 'SNUID': '303E2B7EA5A18C7FC34ADA49A5B77A0D;', 'ABTEST': '0|1453386418|v1', 'CXID': 'D51D5E600468B0E90F70573937FB3A3E', 'SUV': '0096744BDB8E9B9456A114B4D9568399', 'PHPSESSID': 'bevobnbosau8picf198jcag1u2', 'IPLOC': 'CN1100', 'ppinf': '5|1453397172|1454606772|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3MTcyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8', 'refresh': '1', 'weixinIndexVisited': '1'},
    'sanyuanmilk@fleckens.hu': {'ppmdig': '1453396742000000f86d8b8b97a1eadaaaa73bf1af62a9ff', 'ad': 'ZYENXlllll2QoSF@lllllVzPVyGlllllLcfbOlllll6lllllVgDll5@@@@@@@@@@', 'SUIR': '1453397255', 'SUID': '949B8EDB2A10950A0000000056A114FE', 'pprdig': 'GDxSWxb_kipE0dBTgkYhCqDZH7ULWhsgiTp5N3EdouWQTYZNb64VlWzfwvUQtpTrU5X1rojFYH5094M1zNxkEgyjV-L-roRFL9dJXX4_wy8ZTYIsUIX7j2DGRNvRp9G8EfpnDMQ61HE5a5mMarfRPpPItvmZNzceoj1b1BsznAI', 'SNUID': 'A1AEB8ED36331FED5DB5229336853F78;', 'ABTEST': '0|1453386418|v1', 'CXID': 'B4B21B3D4BB68FCB64219E2B3F3EC19F', 'SUV': '0034744DDB8E9B9456A114FE76464532', 'PHPSESSID': 'bevobnbosau8picf198jcag1u2', 'IPLOC': 'CN1100', 'ppinf': '5|1453397246|1454606846|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3MjQ2fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzYW55dWFubWlsa0BmbGVja2Vucy5odXx1bmlxbmFtZTowOnw', 'weixinIndexVisited': '1'},
}


referers = ('http://weixin.sogou.com/',
            'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
            'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
            )



