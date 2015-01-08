from top.api import ItemGetRequest
from top import appinfo 
import json

class TaobaoItem():
    ALL_FIELDS = 'detail_url,num_iid,title,nick,type,cid,seller_cids, \
                   props,input_pids,input_str, \
                   pic_url,num,valid_thru,list_time,delist_time,\
                   stuff_status,location,price,post_fee,express_fee,\
                   ems_fee,has_discount,freight_payer,has_invoice,\
                   has_warranty,has_showcase,modified,increment,approve_status,\
                   postage_id,product_id,auction_point,property_alias,item_imgs,\
                   prop_imgs,skus,videos,outer_id,is_virtual,wap_detail_url,sku, item_img'
    COMMON_FIELDS = 'detail_url,num_iid,title,nick,cid,pic_url,num,list_time,stuff_status,location,price,item_imgs,item_img'
    def __init__(self, app_key, app_secret):
        self.req = ItemGetRequest() 
        self.req.set_app_info(appinfo(app_key, app_secret))

    
    def get_item(self, num_iid, fields = None):
        num_iid = unicode(num_iid)
        if not fields:
            self.req.fields = self.COMMON_FIELDS
        else:
            self.req.fields = fields
        self.req.num_iid = num_iid
        try:
            resp = self.req.getResponse()
            return resp
        except Exception, e:
            print e
            return None

