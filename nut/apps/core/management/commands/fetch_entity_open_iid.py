# coding=utf-8
import json

from django.core.management.base import BaseCommand

from apps.core.models import Buy_Link
import top.api


class Command(BaseCommand):

    def handle(self, *args, **options):
        req = top.api.TaeItemsListRequest()
        req.set_app_info(top.appinfo('23093827', '5a9a26e067f33eea258510e3040caf17'))
        req.fields = "title,nick,price"
        for num_iids in Command.get_num_iids():
            print(num_iids)
            req.num_iids = num_iids
            resp = req.getResponse()
            items = resp.get('tae_items_list_response', {}).get('items', {}).get('x_item', [])
            for item in items:
                Buy_Link.objects.filter(origin_id=item['open_id']).update(taobao_open_iid=item['open_iid'],
                                                                          taobao_data=json.dumps(item))
                self.stdout.write(item['title'])

    @staticmethod
    def get_num_iids():
        for index in xrange(200):
            links = Buy_Link.objects.filter(origin_source='taobao.com', taobao_open_iid__isnull=True).order_by('-id')
            start, end = index * 50, (index + 1) * 50
            values = links[start:end]
            if values.exists():
                value_ids = (origin_id.strip('#') for origin_id in values.values_list('origin_id', flat=True))
                yield ','.join(value_ids)
            else:
                continue
