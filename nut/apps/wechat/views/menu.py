from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.conf import settings
from json import loads
import time
import urllib2
import urllib


AppID = getattr(settings, 'WeChatAppID', None)
AppSecret = getattr(settings, 'WeChatAppSecret', None)



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
        f = urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/token?%s' % urllib.urlencode(self.parameters))
        res = loads( f.read() )
        self.access_token = res['access_token']
        self.expires_in = res['expires_in']

    def post_menu(self, access_token, body):
        req = urllib2.Request('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token ,
                              data=body)
        f = urllib2.urlopen(req)
        return f.read()

    def get(self, request, *args, **kwargs):
        self.get_token()
        return self.render_to_response(self.get_context_data())

__author__ = 'edison7500'
