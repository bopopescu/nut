# coding=utf-8
from __future__ import print_function

import re
import requests
from django.core.management.base import BaseCommand

from apps.core.models import Entity, Sub_Category

url = 'http://recapi.datagrand.com/hot/guoku'


class Command(BaseCommand):
    def handle(self, *args, **options):
        cate_id = args[0]
        sub_category_id = cate_id.split('_')[-1].strip()
        sub_category = Sub_Category.objects.get(pk=sub_category_id)
        print(sub_category.title)
        print(u'-'*20)
        params = {
            "appid": "5215121",
            "cateid": cate_id,
        }
        response = requests.get(url=url, params=params)
        related_data = response.json()['recdata']
        related_entity_ids = [data['itemid'] for data in related_data]
        for related_entity_id in related_entity_ids:
            related_entity = Entity.objects.get(pk=related_entity_id)
            print(related_entity.title)

    @staticmethod
    def get_data(entity):

        tags = []
        prog = re.compile(r"#\w+", re.MULTILINE | re.UNICODE)
        for note in entity.notes.all():
            for match in prog.finditer(note.note):
                tags.append(match.group())

        data = {
            'category_name': entity.category.group.title.strip(),
            'sub_category_name': entity.category.title.strip(),
            'top_note': entity.top_note_string.replace(u',', u'，').strip(),
            'tags': ' '.join(tags) if tags else '-'
        }
        return data
