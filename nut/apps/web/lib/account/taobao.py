import urllib
import urllib2
from urllib import urlencode
from apps.core.utils.taobaoapi.user import TaobaoUser, TaobaoOpenUid, TaobaoOpenIsvUID
from apps.core.utils.taobaoapi.utils import *
import json

TAOBAO_TOKEN_URL = 'https://oauth.taobao.com/token'


class TaobaoClient(object):
    def __init__(self, code, app_key, app_secret):
        self.app_key = app_key
        self.code = code
        self.app_secret = app_secret
        self.redirect_uri = "http://www.guoku.com"

    def get_post_data(self):
        param = {'grant_type': 'authorization_code', 'code': self.code, 'client_id': self.app_key,
                 'client_secret': self.app_secret, 'redirect_uri': self.redirect_uri, 'view': 'web'}
        return param

    def get_res(self):
        param = urllib.urlencode(self.get_post_data())
        token_url = TAOBAO_TOKEN_URL
        res = urllib2.urlopen(token_url, param)
        data = res.read()
        return data


def _get_oauth_url(action, back_url):
    param = {'client_id': APP_KEY, 'response_type': 'code',
             'redirect_uri': back_url, 'view': 'web'}
    return "%s?%s" % (action, urlencode(param))


def get_taobao_user_info(access_token):
    return TaobaoUser(APP_KEY, APP_SECRET).get_user(access_token)


def get_taobao_open_uid(user_id):
    return TaobaoOpenUid(APP_KEY, APP_SECRET).get_open_id(user_id)


def get_taobao_isv_uid(open_uid):
    return TaobaoOpenIsvUID(APP_KEY, APP_SECRET).get_isv_uid(open_uid)


def get_auth_data(code):
    auth_client = TaobaoClient(code=code,
                               app_key=APP_KEY,
                               app_secret=APP_SECRET)
    auth_record = json.loads(auth_client.get_res())
    taobao_user = get_taobao_user_info(auth_record['access_token'])
    open_uid = get_taobao_open_uid(auth_record['taobao_user_id'])
    isv_uid = get_taobao_isv_uid(open_uid)
    log.info(open_uid)
    taobao_data = {'access_token': auth_record['access_token'], 'refresh_token': auth_record['refresh_token'],
                   'taobao_id': auth_record['taobao_user_id'], 'expires_in': auth_record['expires_in'],
                   'screen_name': taobao_user['nick'], 'avatar_large': taobao_user['avatar'], 'open_uid': open_uid,
                   'isv_uid': isv_uid}
    return taobao_data


def get_login_url():
    return _get_oauth_url(OAUTH_URL, CALLBACK_URL)
