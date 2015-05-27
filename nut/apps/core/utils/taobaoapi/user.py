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

<<<<<<< HEAD
class BaichuanUid():
=======

class TaobaoOpenIsvUID():

>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
    def __init__(self, app_key, app_secret):
        self.req = OpensecurityIsvUidGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

<<<<<<< HEAD
    def change_openuid(self, uid):
        self.req.open_uid = uid
=======
    def get_isv_uid(self, open_uid):
        self.req.open_uid = open_uid
>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
        try:
            resp = self.req.getResponse()
            print resp
        except Exception, e:
<<<<<<< HEAD
            print e.message
            raise
        # if (resp.has_key('opensecurity_isv_uid_get_response')):
        #     return resp['opensecurity_isv_uid_get_response']['open_uid_isv']



if __name__=="__main__":
    t = TaobaoOpenUid('12313170', '90797bd8d5859aac971f8cc9d4e51105')
    open_uid = t.get_open_id('56454267')
    print open_uid
    # t.get_open_uid('72913763')
    #
    b = BaichuanUid('12313170', '90797bd8d5859aac971f8cc9d4e51105')
    print b.change_openuid('AAEM6ZQCAASs0HrMGWO7bvZ-')

    c = BaichuanUid('23093827', '7db5a8b0fb21e5d3b9910bf8b9feba38')
    print  c.change_openuid('AAEELit1AB1sujxQQZ64d8D1')

    # b = BaichuanUid('12313170', '90797bd8d5859aac971f8cc9d4e51105')
    # print b.change_openuid('AAEELit1AB1sujxQQZ64d8D1')
=======
            print e

        if (resp.has_key('opensecurity_isv_uid_get_response')):
            return resp['opensecurity_isv_uid_get_response']['open_uid_isv']

if __name__=="__main__":
    t = TaobaoOpenIsvUID('12313170', '90797bd8d5859aac971f8cc9d4e51105')
    open_uid = t.get_isv_uid('AAEa6ZQCAASs0HrMGWO8Wjpb')
    print open_uid
    # t.get_open_uid('72913763')

>>>>>>> 72e43586aba0244e68985f37dafbfd46d5a59172
