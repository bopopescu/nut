import urllib
import urllib2
from urllib import urlencode
from apps.core.utils.taobaoapi.user import TaobaoUser
from apps.core.utils.taobaoapi.utils import *



TAOBAO_TOKEN_URL = 'https://oauth.taobao.com/token'

class TaobaoClient():

    def __init__(self, code, app_key, app_secret):
        self.app_key = app_key
        self.code = code
        self.app_secret = app_secret
        self.redirect_uri = "http://www.guoku.com"

    def get_post_data(self):
        param = {}
        param['grant_type'] = 'authorization_code'
        param['code'] = self.code
        param['client_id'] = self.app_key
        param['client_secret'] = self.app_secret
        param['redirect_uri'] = self.redirect_uri
        param['view'] = 'web'
        return param

    def get_res(self):
        param = urllib.urlencode(self.get_post_data())
        token_url = TAOBAO_TOKEN_URL
        res = urllib2.urlopen(token_url, param)
        data = res.read()
        return data

def _get_oauth_url(action, back_url):
    param = {'client_id' : APP_KEY, 'response_type' : 'code',
             'redirect_uri' : back_url, 'view' : 'web'}
    return "%s?%s" % (action, urlencode(param))

def get_taobao_user_info(access_token):
    return TaobaoUser(APP_KEY, APP_SECRET).get_user(access_token)

def get_auth_data(code):
    auth_client = TaobaoClient(code = code,
                               app_key = APP_KEY,
                               app_secret = APP_SECRET)
    auth_record = json.loads(auth_client.get_res())
    taobao_user = get_taobao_user_info(auth_record['access_token'])
    taobao_data = {}
    taobao_data['access_token'] = auth_record['access_token']
    taobao_data['taobao_id'] = auth_record['taobao_user_id']
    taobao_data['expires_in'] = auth_record['expires_in']
    taobao_data['screen_name'] = taobao_user['nick']
    taobao_data['avatar_large'] = taobao_user['avatar']
    return taobao_data

def get_login_url():
    return _get_oauth_url(OAUTH_URL, CALLBACK_URL)

__author__ = 'edison'
