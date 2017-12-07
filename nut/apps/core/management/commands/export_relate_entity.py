# coding=utf-8
from __future__ import print_function

import re
import requests
from django.core.management.base import BaseCommand

from apps.core.models import Entity

url = 'http://recapi.datagrand.com/relate/guoku'


class Command(BaseCommand):
    def handle(self, *args, **options):
        entity_id = args[0]
        try:
            entity = Entity.objects.get(pk=entity_id)
            entity_data = Command.get_data(entity)
            print('____'.join([
                entity.title,
                entity_data['category_name'],
                entity_data['sub_category_name'],
                entity_data['top_note'],
                entity_data['tags']
            ]))
            print(u'-' * 20)
        except Entity.DoesNotExist:
            print('entity not exist')
            return

        params = {
            "appid": "5215121",
            "itemid": entity_id,
        }
        response = requests.get(url=url, params=params)
        related_data = response.json()['recdata']
        related_entity_ids = [data['itemid'] for data in related_data]
        for related_entity_id in related_entity_ids:
            related_entity = Entity.objects.get(pk=related_entity_id)
            related_entity_data = Command.get_data(related_entity)
            print('____'.join([
                related_entity.title,
                related_entity_data['category_name'],
                related_entity_data['sub_category_name'],
                related_entity_data['top_note'],
                related_entity_data['tags']
            ]))

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
