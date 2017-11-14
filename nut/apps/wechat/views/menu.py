# coding=utf-8
import json
import time

import requests
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

AppID = getattr(settings, 'WECHAT_APP_ID', None)
AppSecret = getattr(settings, 'WECHAT_APP_SECRET', None)


class MenuCreateView(TemplateResponseMixin, ContextMixin, View):
    template_name = 'wechat/menu.html'
    parameters = {
        'appid': AppID,
        'secret': AppSecret,
        'grant_type': 'client_credential',
    }
    _access_token = None
    _expires_in = None

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, value):
        self._expires_in = time.time() + value

    def get_token(self):
        self.access_token = cache.get('wechat_access_token')
        if self.access_token:
            return self.access_token

        r = requests.get("https://api.weixin.qq.com/cgi-bin/token", params=self.parameters)

        res = r.json()
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        cache.set('wechat_access_token', self.access_token, 7200)
        return self.access_token

    def post_menu(self, access_token, body):
        json_string = json.dumps(body, ensure_ascii=False)
        headers = {'content-type': 'application/json'}
        r = requests.post(
            'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token,
            data=json_string, headers=headers)

        return r.text

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        access_token = self.get_token()

        data = {
            "button": [
                {
                    "name": "Pod Shop",
                    "type": "view",
                    "url": "https://h5.youzan.com/v2/showcase/homepage?kdt_id=19312503&reft=1508808840019&spm=f48404986",
                },
                {
                    "name": "每日精选",
                    "type": "view",
                    "url": "http://guoku.com/selected/",
                },
                {
                    "name": "App下载",
                    "sub_button": [
                        {
                            "name": "iPhone下载",
                            "type": "view",
                            "url": "https://itunes.apple.com/cn/app/guo-ku/id477652209?mt=8",
                        },
                        {
                            "name": "Android下载",
                            "type": "view",
                            "url": "http://a.app.qq.com/o/simple.jsp?pkgname=com.guoku",
                        },
                        {
                            "name": "商务合作",
                            "type": "click",
                            "key": "CLICK_CONTACT_US"
                        },
                        {
                            "name": "添加果库妹",
                            "type": "click",
                            "key": "CLICK_APPLY"
                        }
                    ]
                }
            ]
        }

        res = self.post_menu(access_token=access_token, body=data)
        return HttpResponse(res)
