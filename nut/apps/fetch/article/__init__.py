# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
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
sogou_cookies = {'SUV=00101B3C7819479556AE25F1E786A182; ppinf=5|1454253562|1455463162|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjUzNTYyfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpzaG9lbWFoNTVAc3VwZXJyaXRvLmNvbXx1bmlxbmFtZTowOnw; pprdig=Mk0oRUm-R388B8HUHuDLf6OrTR6Trnp2gqpkRH_jTRqx0pWFFGzQWnTlJYzyLwMEpbQauorN1aTKi_DfkSLNu14tMnX9x1DPxVG0TEyIXtuVTdlYG36IPnG9ZDajdu5V049RIKTxElpwszVyU1aZvK-ezaWqquX2_o6iYjlylWg; ABTEST=0|1454253566|v1; ppmdig=1454253566000000ffe7c746a228504a6621d7cb7bf07362; SUID=954719782708930A0000000056AE25FE; SNUID=A576284931351A92FBC566EF311078AB; SUID=954719784FC80D0A0000000056AE260B; IPLOC=CN1100'
                 : 'shoemah55@superrito.com',

                 'ABTEST=0|1454253893|v1; SUID=DE5E09776B20900A0000000056AE2745; SUV=001917E077095EDE56AE275A42C07825; SUID=DE5E09773428950A0000000056AE275A; ppinf=5|1454253924|1455463524|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDU0MjUzOTI0fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMTptb25hbjE5NzdAZmxlY2tlbnMuaHV8dW5pcW5hbWU6MDp8; pprdig=v43xmJG2uTrN735VgGJ7IOxrxi-HZOZuQZIDmAX9WuV27xgf30UyiYPFmtw1csBHmNftCfVmt0SGii27rIbx6QTMI-zL-mGUWgkC7LGqDwmNh3QNQoI2PObeFijLu2j_U5Rj3dUyjsXBsE7fbG89egllpAk8a1Yp4agox21KTtM; CXID=5ADB6A991AF1C95BD9B30FC879C539E6; ad=wJiddyllll2QrANulllllVzmJL7lllllNZOWTkllllYlllll4TDll5@@@@@@@@@@; SNUID=E764334D3A3F139BD8AF2F113A477CD8; ppmdig=1454253941000000c3691e0a8c73ea50aa9fabb7ac01ba3c; IPLOC=CN4300'
                 : 'monan1977@fleckens.hu',

                 'ABTEST=7|1454254207|v1; SNUID=18DB1170090C23ABF9797DE50970CF4B; SUID=11D219786F1C920A0000000056AE287F; SUID=11D2197866CA0D0A0000000056AE2880; SUV=1454254211214178; uuidName=9343b38dd6fc42d3834ba46c0bbc4985; ppinf=5|1454254248|1455463848|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjU0MjQ4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNjpvYnNvbWVkMTk3N0Bqb3VycmFwaWRlLmNvbXx1bmlxbmFtZTowOnw; pprdig=Ewwzj7X-yTJZFgmf8kNMoWb3jjv1N7xTQWtf-NiKrWgHqObOhQGGmnA0caEPj8ZYrfFVJf9C2iCyJju-wlFpd8ASVbwukdb0w87CrAmvqtLpC5MGXXumryViLfkv-Z-Gce1Vr1RcbW7Givg9rSKmLbKFNKIK9mqPQ6M5ubJVEag; CXID=E785645C5E2831BC4BDF2C5838525A49; ad=OcENSlllll2QrAAmlllllVzm3aGlllllWxXv9yllllYlllll4TDll5@@@@@@@@@@; ppmdig=145425426400000039bd8d64920128adf20abf4661e2f79b; IPLOC=CN3100'
                 : 'obsomed1977@jourrapide.com',

                 'uuidName=502d5e921f9946199bda1cf3f679f207; SUV=00B668227819D21156AE28E7C0EBD273; ppinf=5|1454254348|1455463948|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjU0MzQ4fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNTpmaW5pZ2hib3k3OEBzdXBlcnJpdG8uY29tfHVuaXFuYW1lOjA6fA; pprdig=bod48l1o1KxE851z0Q_5wQM1h3P7zvvC3ApSbudtPp7_KtSYPGUtCKBsrRYNuI7ahS_ESsKQFZL3TAtWB55mfpOeKlw6jFyM3tLcipSZZNq6LCuzqph6DgHrZYMZnBA-xshQWyHmfmODMe7YvLKhwokqoXqGVACDMR0uRR_BU2Y; ABTEST=8|1454254392|v1; SNUID=34F63D5C25200E87D850D00F252D8D78; ppmdig=1454254392000000e1599d1eec7d1f5a849c7b4ecd9ffc3f; SUID=11D219786F1C920A0000000056AE2938; IPLOC=CN4403; SUID=11D2197866CA0D0A0000000056AE2939'
                 : 'finighboy78@superrito.com',

                 'uuidName=59a1d206f23d49139a52b31743fd0869; SUV=00E455447819D21156AE29767C702953; ppinf=5|1454254479|1455464079|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjU0NDc5fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyNjphcnRpbWVzc2lsbDE5NTlAZWlucm90LmNvbXx1bmlxbmFtZTowOnw; pprdig=EozTeRczkUY_oEmAT450sqorUb_JhVZP9WgU-D2Ju7B4zzhU_ALiAJoEbGZcTN2YRdq2LQ4VJcvO6ty8MLj3aEoNThYwrf3uxhAuI_FTZmttWpefHNVwx5omSB8lluSA1Csk5sUERR0OAPsvpokgBigx9J03FfQ2X_Pcu2jwHys; ABTEST=0|1454254483|v1; SNUID=79BA7110686242C4668084E2681BFAD2; ppmdig=14542544830000002dceaae281f7e971cffb0247c32893c4; SUID=11D219786F1C920A0000000056AE2993; IPLOC=CN4403; SUID=11D2197866CA0D0A0000000056AE2995'
                 : 'artimessill1959@einrot.com',

                 'ppinf=5|1454254624|1455464224|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjU0NjI0fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjpzdWlsZHJ1ZWQ0MUBkYXlyZXAuY29tfHVuaXFuYW1lOjA6fA; pprdig=ZCN98do5fa2Wisft7-zOXWJpXRjkEpTyyduZ0u8BjbD5rXhNJh0uyyoXWcPQSyNuG4IhL5Gn63ARVtA_TFVCUsncs4-nm-Pc3Fi-mfpPaEaI0MOmQ_nW5rwYVntXAAtX5dRpOu-UQsjt8yLKEvI_s6uhbuXEDNmA-QyueT2N3bA; SUV=00525FA27819D21156AE2A2144027876; ABTEST=5|1454254629|v1; SNUID=87458EEF9793BC359D0C679F97907863; ppmdig=1454254629000000df4976a49605dbb9aa2b59658ac28343; SUID=11D219786F1C920A0000000056AE2A25; IPLOC=CN3301'
                 : 'suildrued41@dayrep.com',

                 'SUID=DE5E09773428950A0000000056AE2855; SUV=0043100677095EDE56AE28558377A534; CXID=F110CBF5CF6C7C1EAED050912A6BEDEA; uuidName=e9c51811b3714d92aee4f11d44fd9db2; ppinf=5|1454254233|1455463833|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDU0MjU0MjMzfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMDphdGVyMTk1NEB0ZWxld29ybS51c3x1bmlxbmFtZTowOnw; pprdig=hP7nC7vQFD6oafRA9Wwi7f7i5MAotdRjWGbK2h-23WPAAW-tR3XINpWe8D5Gw41XIQ3VQzZ8rExpj16XIdvQ1fhMfcm9-GHhzjOhwNlVvfMn9kYgxv-c6659WdNokkthfxaagT9lAe4rmB7lLF6vQJs9_MRixdOpuEspnvd2ggQ; ABTEST=6|1454254301|v1; SNUID=DEA10988FF05D5A208F09ED70030A5DC; ppmdig=1454254301000000c145929ffeb06cc2a1f4a6b7ac49fcd7; IPLOC=CN8100; weixinIndexVisited=1; ad=BUcY@Zllll2QrAPQlllllVzm3nGlllllNZOWTkllllclllll4TDll5@@@@@@@@@@'
                 : 'ater1954@teleworm.us',

                 'uuidName=b001425f4c8541b8b3020a7eaf876000; SUV=00975FA17819D21156AE2AA3E9B38186; ABTEST=0|1454254799|v1; SNUID=4B8942235B5F71F84FE4403E5BF07B03; SUID=11D219786F1C920A0000000056AE2ACF; SUID=11D2197866CA0D0A0000000056AE2AD0; ppinf=5|1454254820|1455464420|Y2xpZW50aWQ6NDoxMTIwfGNydDoxMDoxNDU0MjU0ODIwfHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpkdWFkMTkzN0Bqb3VycmFwaWRlLmNvbXx1bmlxbmFtZTowOnw; pprdig=HX5o_G4GsLsz_iMdxrBnrQv6ZdnwQPurVW0J56vgU2q_2yPoQNhQ95MDuDqDUVdk7u7pkBth87BmVdmP7qrSbXuufalslvpZTiQDu7qt9QjO0lkOQL8zkGIm4Gow3MwKvQUwGpvMtZs7w_Z9S8gAzV0W1iip5ZeH95A9xaqo7Vg; ppmdig=1454254826000000cee009f27d84f55baa9241eccacc984c; IPLOC=CN4403'
                 : 'duad1937@jourrapide.com',

                 'uuidName=809c80f307f043ba86cdbe94806b1268; SUV=00835FA077095EDE56AE291EEA433126; ppinf=5|1454254635|1455464235|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDU0MjU0NjM1fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMjpkcmVjdXI0NEBzdXBlcnJpdG8uY29tfHVuaXFuYW1lOjA6fA; pprdig=l87mncvUbPBdx80QCFdcpPTZmsAAwpKAd8tQGU0kAMD81v_UthvNL7_H94-QN-OnlQ1XjIC4VSUZEfD0uua93AmH5rthQ-K8vIy5FNpGsCDA7YH-WUmal3W_2VVRnpWnb-c71u15otkP4B1qOxYN_uvxg9nyIZMEJsG2htDVEi0; SUID=11D219783528950A0000000056AE2A31; CXID=6037FD4079FF11227250952E7149F06B; ABTEST=0|1454254663|v1; ppmdig=1454254663000000cf5338020bdcc6351de2c0ef8053e6f9; weixinIndexVisited=1; SNUID=0BC903631A1F30B917C724501BB2503C; IPLOC=CN3301; LSTMV=296%2C29; LCLKINT=1909; ad=WdEd@Zllll2QrAohlllllVzm3OllllllWxXv9yllllZlllll4TDll5@@@@@@@@@@'
                 : 'drecur44@superrito.com',

                 'uuidName=09bcbd7f40a14f929967f0eaee538962; SUV=002670817819D21156AE2A92E239D289; ppinf=5|1454254764|1455464364|Y2xpZW50aWQ6NDoyMDA2fGNydDoxMDoxNDU0MjU0NzY0fHJlZm5pY2s6MDp8dHJ1c3Q6MToxfHVzZXJpZDoyMzpwYWJveTE5NzNAc3VwZXJyaXRvLmNvbXx1bmlxbmFtZTowOnw; pprdig=x9psI3un3yS3OTJJN0bD08vltwugiawAyPX-QHISnHCNSSaEz8pWAx-cKmenTGYAkPHGOAAvy2fY0o8Vbhvyy7ZpWCm3fT9rDNTxmAixXDNBLNjOnnNTK0Q_RmsZchbs4OTblFOM0J5wN4TteFe4TDbthcNru28b0rNt323j_dk; SUID=11D219783528950A0000000056AE2AB0; CXID=C58B5E95B894AB24F890B3307C6A3733; ABTEST=0|1454254777|v1; ppmdig=14542547770000002c2d638f7424dcc6c82b16943c5f3e7a; weixinIndexVisited=1; SNUID=814389E99195BB328336EE90912D5BA1; IPLOC=CN3301; ad=WDiNSZllll2QrA$3lllllVzm37klllllWxXv9ylllxllllll4TDll5@@@@@@@@@@'
                 : 'paboy1973@superrito.com'
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
