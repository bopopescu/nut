from django.conf import settings
from django.core.cache import cache
from item import TaobaoItem
from shop import TaobaoShop
from taobaoke import TaobaokeMobileItem
from hashlib import md5
# import json

from django.utils.log import getLogger

log = getLogger('django')

APP_KEY = getattr(settings, "TAOBAO_APP_KEY", None)
APP_SECRET = getattr(settings, "TAOBAO_APP_SECRET", None)
CALLBACK_URL = getattr(settings, "TAOBAO_BACK_URL", None)
OAUTH_URL = getattr(settings, "TAOBAO_OAUTH_URL", None)
OAUTH_LOGOFF_URL = getattr(settings, "TAOBAO_OAUTH_LOGOFF", None)

def load_taobao_item_info_from_api(taobao_id):
    taobao = TaobaoItem(APP_KEY, APP_SECRET)
    res = taobao.get_item(taobao_id)
    try:
        return res['item_get_response']['item']
    except:
        return None

def load_taobao_shop_info_from_api(shop_nick):
    shop = TaobaoShop(APP_KEY, APP_SECRET)
    return shop.get_shop_info(shop_nick)

def taobaoke_mobile_item_convert(num_iid, outer_code = "", fields = None):
    key_string = 'taobaoke_%s' % num_iid
    key = md5(key_string.encode('utf-8')).hexdigest()

    url = cache.get(key)
    if url:
        return url
    request = TaobaokeMobileItem(APP_KEY, APP_SECRET)
    res = request.convert_items(num_iid, outer_code)
    log.info(res)

    try:
        url = res['tbk_mobile_items_convert_response']['tbk_items']['tbk_item'][0]
        cache.set(key, url, timeout=86400)

    except KeyError, e:
        log.error("Error: %s" % e.message)
        return None

    return url
