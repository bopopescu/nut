#coding=utf-8
from top.api import ShopGetRequest
from top import appinfo
import json

class TaobaoShop():

    def __init__(self, app_key, app_secret):
        self.req = ShopGetRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))


    def get_shop_info(self, nick, fields = None):
        self.req.nick = nick
        if not fields:
            self.req.fields = "sid,cid,nick,title,pic_path,created,modified,shop_score"
        else:
            self.req.fields = fields
        try:
            print "get"
            resp = self.req.getResponse()
            print resp
            return resp['shop_get_response']['shop']
        except Exception, e:
            print e
            return None

