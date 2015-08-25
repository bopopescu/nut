#coding: utf-8
from top.api import UserBuyerGetRequest
from top.api import OpensecurityUidGetRequest, OpensecurityIsvUidGetRequest
from top import appinfo

# import json

import logging

logger = logging.getLogger('django.request')


class TaobaoUser():

    def __init__(self, app_key, app_secret):
        self.req = UserBuyerGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def get_user(self, session_key):
        self.req.fields = 'user_id,nick,sex,location,birthday,email,alipay_account,avatar'
        res = self.req.getResponse(session_key)
        logger.info(res)
        if res.has_key('user_buyer_get_response'):
            return res['user_buyer_get_response']['user']
        return None


class TaobaoOpenUid():
#
    def __init__(self, app_key, app_secret):
        self.req = OpensecurityUidGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def get_open_id(self, user_id):
        self.req.tb_user_id = user_id
        try:
            resp= self.req.getResponse()
            # print resp
        except Exception, e:
            print e.message
            return None
        if (resp.has_key('opensecurity_uid_get_response')):
            return resp['opensecurity_uid_get_response']['open_uid']


class TaobaoOpenIsvUID():

    def __init__(self, app_key, app_secret):
        self.req = OpensecurityIsvUidGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def get_isv_uid(self, open_uid):
        self.req.open_uid = open_uid

        try:
            resp = self.req.getResponse()
            # print resp
        except Exception, e:
            print e
            raise

        if (resp.has_key('opensecurity_isv_uid_get_response')):
            return resp['opensecurity_isv_uid_get_response']['open_uid_isv']



if __name__=="__main__":
    t = TaobaoOpenIsvUID('23093827', '5a9a26e067f33eea258510e3040caf17')
    open_uid = t.get_isv_uid('AAEELit1AB1sujxQQZ64d8D1')
    print open_uid


    # from apps.core.models import Taobao_Token
    #
    # taobao = Taobao_Token.objects.get(user_id = 1062)
    # print taobao
    # t.get_open_uid('72913763')

