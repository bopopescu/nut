# coding=utf-8
from __future__ import print_function

import re

from django.core.management.base import BaseCommand

from apps.core.models import Entity


class Command(BaseCommand):
    help = 'clean all blocked user\'s data'

    def handle(self, *args, **options):
        entity_ids = []
        with open('data/entity_ids.txt') as f:
            entity_ids = [entity_id.strip() for entity_id in f]

        for entity_id in entity_ids:
            try:
                entity = Entity.objects.get(pk=entity_id)
                entity_data = Command.get_data(entity)
                print(u','.join([
                    entity_id,
                    entity_data['category_name'],
                    entity_data['sub_category_name'],
                    entity_data['top_note'],
                    entity_data['tags'],
                ]))
            except Entity.DoesNotExist:
                print(u'{},-,-,-,-,'.format(entity_id))

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
            'top_note': entity.top_note_string.strip().replace(u',', u'，').replace(u'\n', u' '),
            'tags': ' '.join(tags) if tags else '-'
        }
        return data
