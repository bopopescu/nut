# coding=utf-8
from __future__ import print_function

import pprint
import re

import requests
from django.core.management.base import BaseCommand
from django.db.models import Count, datetime

from apps.core.models import Entity


url = 'http://datareportapi.datagrand.com/data/guoku'


class Command(BaseCommand):
    def handle(self, *args, **options):

        price_ranges = [
            (1, 100, 3000),
            (100, 200, 3000),
            (200, 500, 3000),
            (500, 1000, 1000),
        ]

        for start, end, amount in price_ranges:
            entities = Entity.objects.filter(
                status__gte=0,
                created_time__gte='2015-01-01',
                price__gte=start,
                price__lt=end,
                notes__isnull=False,
            )

            entities = entities.select_related('likes').annotate(like_count_zz=Count('likes')).order_by(
                '-like_count_zz')

            for entity in entities[:amount]:
                entity_data = Command.get_data(entity)
                payload = {
                    'appid': '5215121',
                    'table_name': 'item',
                    'table_content': [{'cmd': 'add', 'fields': entity_data}]
                }
                response = requests.post(url, json=payload)
                print(response.text)
                # pprint.pprint(entity_data)

    @staticmethod
    def get_data(entity):

        tags = []
        prog = re.compile(r"#\w+", re.MULTILINE | re.UNICODE)
        for note in entity.notes.all():
            for match in prog.finditer(note.note):
                tags.append(match.group())

        data = {
            'itemid': entity.id,
            'cateid': u'_'.join([unicode(entity.category.group.id), unicode(entity.category.id)]),
            'title': entity.title,
            'content': entity.top_note_string.replace(u',', u'，').strip(),
            'price': int(entity.price * 100),
            'item_tags': u';'.join(tags),
            'item_modify_time': int((entity.updated_time - datetime.datetime(1970, 1, 1)).total_seconds()),
        }
        return data
