# coding=utf-8
import json
from pprint import pprint

from django.core.management.base import BaseCommand

from apps.core.models import Buy_Link, TaobaoCategory
import top.api


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Command(BaseCommand):
    help = 'fetch taobao category data'

    def handle(self, *args, **options):
        req = top.api.ItemcatsGetRequest()

        req.set_app_info(top.appinfo('23093827', '5a9a26e067f33eea258510e3040caf17'))
        req.fields = "cid,parent_cid,name,is_parent,features"

        all_cids = Buy_Link.objects.values_list('cid', flat=True).distinct()
        all_cids = list(all_cids)

        for cids in chunks(all_cids, 20):
            req.cids = ','.join(cid for cid in cids if cid)
            print(req.cids)
            try:
                resp = req.getResponse()
                category_items = resp.get('itemcats_get_response', {}).get('item_cats', {}).get('item_cat', [])
                for category_item in category_items:
                    payload = {
                        'cid': category_item['cid'],
                        'parent_cid': category_item['parent_cid'],
                        'name': category_item['name'].encode('utf-8'),
                        'is_parent': category_item['is_parent'],
                        'json_data': json.dumps(category_item, encoding='utf-8')
                    }
                    try:
                        category = TaobaoCategory.objects.create(**payload)
                        print(category.name)
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
