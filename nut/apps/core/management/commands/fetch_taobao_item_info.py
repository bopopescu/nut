# coding=utf-8
import json

from django.core.management.base import BaseCommand

from apps.core.models import Buy_Link, TaobaoItem
import top.api


class Command(BaseCommand):
    help = 'fetch taobao item data'

    def handle(self, *args, **options):
        req = top.api.TaeItemDetailGetRequest()
        req.set_app_info(top.appinfo('23093827', '5a9a26e067f33eea258510e3040caf17'))
        req.fields = ','.join([
            'itemInfo', 'priceInfo', 'skuInfo', 'stockInfo', 'rateInfo', 'descInfo', 'sellerInfo', 'mobileDescInfo',
            'deliveryInfo', 'storeInfo', 'itemBuyInfo', 'couponInfo'
        ])

        links = Buy_Link.objects.filter(origin_source='taobao.com', taobao_open_iid__isnull=False)
        links = links.filter(taobao_items__isnull=True)

        for link in links:
            req.open_iid = link.taobao_open_iid
            try:
                resp = req.getResponse()
                item_data = resp.get('tae_item_detail_get_response', {}).get('data', {})
                payload = {
                    'buy_link_id': link.id,
                    'open_iid': link.taobao_open_iid,
                    'origin_id': link.origin_id,
                    'seller_type': item_data.get('seller_info', {}).get('seller_type', '').encode('utf-8'),
                    'seller_nick': item_data.get('seller_info', {}).get('seller_nick', '').encode('utf-8'),
                    'title': item_data.get('item_info', {}).get('title', '').encode('utf-8'),
                    'json_data': json.dumps(resp)
                }
                item = TaobaoItem.objects.create(**payload)
                print(item.title)
            except Exception as e:
                print(e)
