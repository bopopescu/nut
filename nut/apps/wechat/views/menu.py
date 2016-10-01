# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.utils.log import getLogger
from django.core.cache import cache
# from json import loads
import time
# import urllib2
# import urllib
import requests
from django.utils import simplejson
from django.conf import settings

AppID = getattr(settings, 'WECHAT_APP_ID', None)
AppSecret = getattr(settings, 'WECHAT_APP_SECRET', None)

# AppID = settings.WeChatAppID
# AppSecret = settings.WeChatAppSecret


log = getLogger('django')


class MenuCreateView(TemplateResponseMixin, ContextMixin, View):

    template_name = 'wechat/menu.html'
    parameters = {
            'appid': AppID,
            'secret': AppSecret,
            'grant_type': 'client_credential',
        }
    log.info(parameters)
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
        log.info(res)
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']
        cache.set('wechat_access_token', self.access_token, 7200)
        return self.access_token

    def post_menu(self, access_token, body):
        json_string = simplejson.dumps(body, ensure_ascii=False)
        log.info(json_string)
        headers = {'content-type': 'application/json'}
        r = requests.post('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token, data=json_string, headers=headers)

        return r.text

    def get(self, request, *args, **kwargs):

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        # access_token = cache.get('wechat_access_token')
        # if access_token is None:
        access_token = self.get_token()

        data = {
            "button":[
                {
                    "name":"热门精选",
                    "sub_button": [
                        {
                            "name":"每日精选",
                            "type":"view",
                            "url":"http://guoku.com/selected/",
                        },
                        {
                            "name":"热门商品",
                            "type":"view",
                            "url":"http://guoku.com/popular/",
                        },
                        {
                            "name":"更多专题",
                            "type":"view",
                            "url":"http://guoku.com/event/",
                        },
                        {
                            "type": "click",
                            "name": "我的果库",
                            "key": "V2001_USER_LIKE",
                        },
                    ]
                },
                {
                    "name":"线下商店",
                    "sub_button": [
                        {
                            "name": "十一活动",
                            "type": "view",
                            "url": "http://m.guoku.com/articles/135144/"
                        },
                        {
                            "name"  : "服务计划",
                            "type"  : "view",
                            "url"   : "http://m.guoku.com/shopservice/"
                        },
                        {
                            "name"  : "商店列表",
                            "type"  : "view",
                            "url"   : "http://m.guoku.com/articles/134060/"
                        },

                    ]
                },
                {
                    "name":"应用下载",
                    "sub_button": [
                        {
                            "name":"iPhone 版",
                            "type":"view",
                            "url":"https://itunes.apple.com/cn/app/guo-ku/id477652209?mt=8",
                        },
                        {
                            "name":"iPad 版",
                            "type":"view",
                            "url":"https://itunes.apple.com/cn/app/guo-kuhd/id450507565?mt=8",
                        },
                        {
                            "name":"Andorid 版",
                            "type":"view",
                            "url":"http://www.wandoujia.com/apps/com.guoku",
                        }
                    ]
                }
            ]
        }

        res = self.post_menu(access_token=access_token, body=data)
        log.info(res)
        return HttpResponse(res)




__author__ = 'edison7500'
