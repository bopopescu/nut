# coding=utf-8
from __future__ import print_function

import re

from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.core.models import Entity


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

            entities = entities.select_related('likes').annotate(like_count_zz=Count('likes')).order_by('-like_count_zz')
            print(u'-,-,-,-,-,-')

            for entity in entities[:amount]:
                entity_data = Command.get_data(entity)
                print(u','.join([
                    unicode(entity.id),
                    unicode(entity.price),
                    entity_data['category_name'],
                    entity_data['sub_category_name'],
                    entity_data['top_note'],
                    entity_data['tags'],
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
