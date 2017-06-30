# coding=utf-8
import sys
from django.core.management.base import BaseCommand

from apps.core.models import TaobaoItem, TaobaoShop
import top.api

reload(sys)
sys.setdefaultencoding('utf8')


class Command(BaseCommand):
    help = 'fetch taobao shop data'

    def handle(self, *args, **options):
        req = top.api.ShopGetRequest()

        req.set_app_info(top.appinfo('23093827', '5a9a26e067f33eea258510e3040caf17'))
        req.fields = "sid,cid,title,nick,desc,bulletin,pic_path,created,modified, shop_score"

        nicks = TaobaoItem.objects.values_list('seller_nick', flat=True)
        nicks = sorted(list(set(nicks)))

        for nick in nicks:
            if TaobaoShop.objects.filter(nick=nick).exists():
                print('exists')
                continue

            req.nick = nick.encode('utf-8')
            try:
                resp = req.getResponse()
                shop_data = resp.get('shop_get_response', {}).get('shop', {})
                payload = {
                    'sid': shop_data['sid'],
                    'cid': shop_data['cid'],
                    'nick': shop_data['nick'].encode('utf-8'),
                    'title': shop_data['title'].encode('utf-8'),
                    'desc': shop_data['desc'].encode('utf-8'),
                    'pic_path': shop_data['pic_path'],
                    'bulletin': shop_data['bulletin'].encode('utf-8'),
                    'created': shop_data['created'],
                    'modified': shop_data['modified'],
                    'item_score': shop_data['shop_score']['item_score'],
                    'delivery_score': shop_data['shop_score']['delivery_score'],
                    'service_score': shop_data['shop_score']['service_score']
                }
                shop = TaobaoShop.objects.create(**payload)
                print(shop.nick)
            except Exception as e:
                print(nick, e)
