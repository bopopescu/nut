from top.api import TbkMobileItemsConvertRequest
from top import appinfo
import json

class TaobaokeMobileItem():
    ALL_FIELDS = "click_url"

    def __init__(self, app_key, app_secret):
        self.req = TbkMobileItemsConvertRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def convert_items(self, num_iids, outer_code, fields = None):
        self.req.num_iids = num_iids
        self.req.outer_code = outer_code
        if not fields:
            self.req.fields = self.ALL_FIELDS
        else:
            self.req.fields = fields
        try:
            resp = self.req.getResponse()
            return resp
        except Exception, e:
            print e
            return None

'''
class TaobaokeMobileItem():
    ALL_FIELDS = "num_iid,title,nick,pic_url,price,promotion_price,click_url,commission,commission_rate,commission_num,commission_volume,shop_click_url,seller_credit_score,item_location,volume"

    def __init__(self, app_key, app_secret):
        self.req = TaobaokeMobileItemsConvertRequest()
        self.req.set_app_info(appinfo(app_key, app_secret))

    def convert_items(self, num_iids, outer_code, fields = None):
        self.req.num_iids = num_iids
        self.req.outer_code = outer_code
        if not fields:
            self.req.fields = self.ALL_FIELDS
        else:
            self.req.fields = fields
        try:
            resp = self.req.getResponse()
            return resp
        except Exception, e:
            print e
            logger.error("[taobao_api_error][mobile_item_convert_request] %s", e)
            return None
'''
