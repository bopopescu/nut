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
    def __init__(self, countdown=5):
        self.countdown = countdown
        self.message = 'Fetch error, need to login or get new token.'


class Expired(Exception):
    pass


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
            self.refresh_cookies()
            raise Retry
        if result.find(u'当前请求已过期') >= 0:
            log.warning(u'当前请求已过期. url: %s', url)
            raise Expired('link expired: %s' % url)
        if format_json:
            result = self.json_response(resp)
            if 'code' in result and result['code'] == "needlogin":
                self.refresh_cookies()
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

    def refresh_cookies(self):
        self.cookies.clear()
        self.headers['Cookie'] = random.choice(sogou_cookies)
        self.headers['User-Agent'] = faker.user_agent()
        self.headers['Referer'] = random.choice(sogou_referers)

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
            log.error("Json decode error %s", result)
            raise


#############  Cookies  #############
sogou_cookies = (
    "ABTEST=0|1453548272|v1; SNUID=6EB8716D1E1B37E08A6F8B5E1F2450EB; IPLOC=CN1100; SUID=70A76F722624930A0000000056A362F0; SUV=00AE23E7726FA77056A36302D20F7531; SUID=70A76F72523A900A0000000056A36302; CXID=8C34EE0853B2F483AD898F12B3CF930B; ppinf=5|1453548293|1454757893|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTQ4MjkzfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=un7vDTDdsS7WFK81iNlIc6vXJyQZard_Auc5L52-DKNhDjyFQcuK82MvhATuv6RG1GfJMWTxiId4dd7-xDO0npsZiA32Wl_qYU84YtKpsv2vwR2uff5j1DS8kVrF_pOT8YXmO43qM8cWXq7p4Qd65emyRr3DFPCzZ1klK4pFTBs; ad=brcPwkllll2QoLGRlllllVz0YhZlllllzAKWwlllljUlllllVTDll5@@@@@@@@@@",
    "IPLOC=CN1100; SUV=00DD23E4726FA77056A36385C26FF582; SUID=70A76F72523A900A0000000056A36385; CXID=428F7227DC297F7350FCE2DD518F2C4A; ppinf=5|1453548429|1454758029|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTQ4NDI5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxODphbmR1cm5AZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=aT1m4JkxNWh8PYDWqi3PWYbJaI3VNP85bU6jiRaDn1xvyTymoOrRzzKt0EHPhjTI_0EKbHqT8UkJRqlwDZz6W1S5UurnQFiqjKMUeopAS2ZL6yKOgVScNt3MbYAjCThaBlUNSxWP_xaN0LFqE6cxvWI7pFsImV_GuRqgc0lQZCM; ad=@HEdjZllll2QoLnVlllllVz0YcclllllzAKWwlllll7lllllVTDll5@@@@@@@@@@",
    "IPLOC=CN1100; SUV=00DD23E4726FA77056A36404C2DC9318; SUID=70A76F72523A900A0000000056A36404; CXID=0AC090DC88F924223AAFD97F33FC7DC0; ppinf=5|1453548606|1454758206|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTQ4NjA2fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzYW55dWFubWlsa0BmbGVja2Vucy5odXx1bmlxbmFtZTowOnw; pprdig=vYgD15Qj9nDZ2lPcL8Sw7vHe7uC4Biod6LjvAW2NgMnf0xDn2PbulNa_j_3jwAzRMi1TsGIbj4byo4kJY5zLvRuE08I5TBB3_M66lCYk_5bO0Pz8HcJF8V7Jkmw2s3B1eCOSCx9lsg7vyBYRucbtuyiCmXwD5K2AkCBpEXcldqk; ad=X4fO7kllll2QoLyVlllllVz0B9lllllltuMXtllllxwlllllVTDll5@@@@@@@@@@",
    "ABTEST=0|1453397330|v1; PHPSESSID=u7lmaa86vrl9lesn6c5a6ecgb3; SUV=0043744ADB8E9B9456A116DDA028B542; SUID=949B8EDB2A10950A0000000056A116DD; CXID=FC0093A199000C2FE6E765E1003C6F3C; ppinf=5|1453397741|1454607341|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3NzQxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=CJi7Tuix5HauM6vA3bJNUk0Dg7fbqaZ6HXquUkUHlBmoo6fhLqWRW0sel0tjQKQCVjMb19Ep5VLB9uKpo4Qo07SoM5g96XpakviRkZC3AyI6k5J0fO2S3bZEkqWUO7nKj4UuHgkayQ4iB6CaCMkoB75k3z4VUwoVu_BONkfLSsk; ad=ZEfdKkllll2QoSbNlllllVzPVsllllllLcfbOllllxGlllllVgDll5@@@@@@@@@@; SUIR=1453397763; weixinIndexVisited=1; cid=wx2ww; ssuid=2499230992; SNUID=86A797D0505478B7D76E14D6515507F0; ppmdig=1453540590000000e9aff680f424fb8bf4fb3389e526144e; sct=1; IPLOC=CN1100",
    "ABTEST=0|1453548274|v1; IPLOC=CN1100; SUV=008F17DE3CFDB1BE56A36374EB1A1590; SUID=BEB1FD3C3428950A0000000056A36374; CXID=37438510B1E7633E3B70D100FB458781; ppinf=5|1453548420|1454758020|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTQ4NDIwfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=V164tKv2TebB7l9ZQVICO7maVsIzUoQW7DuKg1q3Nldu5P3-OayOvzeR-aEtNHn13QxzzO0qiNPFVZIiVZyPLPiXZ-m0XkEZDYVJ04UQjVHkBQPlJrmIsdX2GfkZ4JeyjCKKfyi4-cxkOVLPTf2sr8DKH8oQdPmfvuPBqHF8RHw; ad=X2EdQZllll2QoL21lllllVz0Yctlllll55LesklllxwlllllVTDll5@@@@@@@@@@; SNUID=D1DF93536E6A4790F2DA07326FC29438; ppmdig=1453548274000000f9ea7bdf7ad4f1f624758340e5de4902",
    "ABTEST=0|1453548274|v1; SNUID=D1DF93536E6A4790F2DA07326FC29438; ppmdig=1453548274000000f9ea7bdf7ad4f1f624758340e5de4902; IPLOC=CN1100; SUV=00E317DC3CFDB1BE56A363AFA64D7409; SUID=BEB1FD3C3428950A0000000056A363AF; CXID=C72CBB7F14F979A5D6826389C1CC31D7; ppinf=5|1453548476|1454758076|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTQ4NDc2fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=I12Z-hk_5skvB6CvcLgnNw2evMwJLohx1gW8QAr4kfqxDJSysMq6lGdgO9ZNwkG8-LhG1Ari9oRw12HWUyteSw6_nEVn0pli5KX05v0664Zm7fyOluj312oSrbtBKGQKAyz2nkJDyQ56J1gESl6oA_cJSxxeSdGpz7TDPk_rRqY; ad=oTfO7kllll2QoLnslllllVz0YEDlllll55LesklllxwlllllVTDll5@@@@@@@@@@"
    'ABTEST=0|1453397330|v1; PHPSESSID=u7lmaa86vrl9lesn6c5a6ecgb3; SUV=0043744ADB8E9B9456A116DDA028B542; SUID=949B8EDB2A10950A0000000056A116DD; CXID=FC0093A199000C2FE6E765E1003C6F3C; ppinf=5|1453397741|1454607341|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzMzk3NzQxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoxOTp3YXNlcjE5NTlAZ3VzdHIuY29tfHVuaXFuYW1lOjA6fA; pprdig=CJi7Tuix5HauM6vA3bJNUk0Dg7fbqaZ6HXquUkUHlBmoo6fhLqWRW0sel0tjQKQCVjMb19Ep5VLB9uKpo4Qo07SoM5g96XpakviRkZC3AyI6k5J0fO2S3bZEkqWUO7nKj4UuHgkayQ4iB6CaCMkoB75k3z4VUwoVu_BONkfLSsk; ad=ZEfdKkllll2QoSbNlllllVzPVsllllllLcfbOllllxGlllllVgDll5@@@@@@@@@@; SUIR=1453397763; weixinIndexVisited=1; cid=wx2ww; ssuid=2499230992; SNUID=86A797D0505478B7D76E14D6515507F0; ppmdig=1453540590000000e9aff680f424fb8bf4fb3389e526144e; sct=1; IPLOC=CN1100; LSTMV=428%2C92; LCLKINT=71417',
    'ABTEST=0|1453548274|v1; weixinIndexVisited=1; ppinf=5|1453551229|1454760829|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTUxMjI5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNzphc29ydGFmYWlyeXRhbGVAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=X4Am8NNTpogMzmMjx7xRW33Rw16qJhaoRouPESLARi59sUsbx0lcVOep2qKwSFGqoYH3Tw7ylMNLcFOIHiyMYsuh4z7m5LrrJLx43va_9SU_f7gfUWhwnUVIfz4e6ya09hdtB1YqwC651Nf-qfERRhmaoA9n3sRBmQX0V2U1sUU; IPLOC=CN1100; SUV=00E317DC3CFDB1BE56A36E7DAC4AD431; SUID=BEB1FD3C3428950A0000000056A36E7D; CXID=291918D768260E6E165593A156BEE78C; ad=eNEd6Zllll2QoLiMlllllVz0bollllll55Leskllll6lllllVTDll5@@@@@@@@@@; SNUID=8B84C80A35301FC970676F14360413FC; ppmdig=145355123900000012839edaa4e12351fe4aec4ed6fa1923',
    'ABTEST=0|1453548274|v1; weixinIndexVisited=1; ppinf=5|1453551361|1454760961|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDUzNTUxMzYxfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjphZGlzYWlkQGpvdXJyYXBpZGUuY29tfHVuaXFuYW1lOjA6fA; pprdig=JUy6ve-X1fdWDQWGEMH9jMV448YiF-NHG5dm3MTSPNmJasMDtuvfo5rgYQIEpTUqmfY3jghcimxj6zxC9sqt5KOf3r-6uT3lfkBCa_z6NSYMsW1FkL1wB1WkVmoAeNkp2rMIGKTOLYyuR0T_go2uxP8S_uCq0kNpW0N3AIRu9D0; IPLOC=CN1100; SUV=008F17DE3CFDB1BE56A36F01F1E13976; SUID=BEB1FD3C3428950A0000000056A36F01; CXID=1F9E4F4E2D3ED2C0479B94D78E6DF27D; ad=xNEdQZllll2QoLDjlllllVz0bZUlllll55Leskllll6lllllVTDll5@@@@@@@@@@; SNUID=DCD09F5E6167489E2C75BEAB6279B4C7; ppmdig=1453551239000000d1141a1665f46262d892708762c9ff19',
)


sogou_referers = ('http://weixin.sogou.com/',
                  'http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&mid=406976557&idx=3&sn=e2749cff6e7fbf1379f4d7ee5829a5aa&3rd=MzA3MDU4NTYzMw==&scene=6#rd',
                  'http://weixin.sogou.com/weixin?type=1&query=a&ie=utf8'
                  )
