#coding: utf-8
from top.api import UserBuyerGetRequest
from top import appinfo
import json
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

