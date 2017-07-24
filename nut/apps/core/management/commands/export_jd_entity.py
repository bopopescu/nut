# coding=utf-8
import csv
from pprint import pprint

from django.core.management.base import BaseCommand

from apps.core.models import Buy_Link


class Command(BaseCommand):

    def handle(self, *args, **options):
        buy_links = Buy_Link.objects.select_related('entity').filter(origin_source='jd.com',
                                                                     entity__status__gte=0)

        data_list = [Command.get_data(buy_link) for buy_link in buy_links]
        pprint(data_list)
        with open('jd_entity.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['entity_name', 'entity_url', 'jd_url', 'brand', 'category', 'price', 'like_count', 'note_count', 'created_time'])
            writer.writeheader()
            writer.writerows(data_list)

    @staticmethod
    def get_data(buy_link):
        return {
            'entity_name': buy_link.entity.title.encode('utf-8'),
            'entity_url': 'http://www.guoku.com{}'.format(buy_link.entity.absolute_url).encode('utf-8'),
            'jd_url': buy_link.link.encode('utf-8'),
            'brand': buy_link.entity.brand.encode('utf-8'),
            'category': buy_link.entity.category_name.encode('utf-8'),
            'price': buy_link.entity.price,
            'like_count': buy_link.entity.like_count,
            'note_count': buy_link.entity.note_count,
            'created_time': buy_link.entity.created_time,
        }
