# coding=utf-8
from __future__ import print_function

import re

import time
from django.core.management.base import BaseCommand

import arrow
from apps.core.models import Entity
from utils.open_search_api import V3Api
from utils.utils import chunks
from django.conf import settings

api = V3Api(endpoint=settings.OPEN_SEARCH_ENDPOINT, access_key=settings.OPEN_SEARCH_ACCESS_KEY_ID,
            secret=settings.OPEN_SEARCH_ACCESS_KEY_SECRET, app_name=settings.OPEN_SEARCH_APP_NAME)


class Command(BaseCommand):

    def handle(self, *args, **options):
        num = int(args[0]) if args else 10
        entities = Entity.objects.filter(
            status__gte=0,
            is_sync=False,
        ).order_by('-created_time')

        for es in chunks(entities, num):
            time.sleep(5)
            entities_data = [Command.get_data(entity) for entity in es]
            entity_ids = [d['id'] for d in entities_data]
            print(u'-' * 20)
            print(u', '.join(unicode(pk) for pk in entity_ids))
            payload = [{'cmd': 'add', 'fields': d} for d in entities_data]
            result = api.bulk_update('entity', payload)
            if result['status'] == u'OK':
                success_entities = Entity.objects.filter(pk__in=entity_ids)
                if 0 < success_entities.count() <= num:
                    update_count = success_entities.update(is_sync=True)
                    print('Success: {}!'.format(update_count))
                else:
                    print('Oh, No!')
            else:
                print(result)

    @staticmethod
    def get_data(entity):

        tags = []
        prog = re.compile(r"#\w+", re.MULTILINE | re.UNICODE)
        for note in entity.notes.all():
            for match in prog.finditer(note.note):
                tags.append(match.group())

        data = {
            'id': entity.id,
            'title': entity.title,
            'intro': entity.top_note_string.replace(u',', u'，').strip(),
            'brand': entity.brand,
            'category_name': entity.category.group.title.strip(),
            'sub_category_name': entity.category.title.strip(),
            'tags': ' '.join(tags) if tags else '-',
            'created_time': arrow.get(entity.created_time).timestamp,
            'status': entity.status,
        }

        return data
