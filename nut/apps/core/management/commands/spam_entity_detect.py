# coding=utf-8
from __future__ import print_function

from django.core.management.base import BaseCommand

from apps.core.models import Entity


class Command(BaseCommand):
    def handle(self, *args, **options):
        keywords = Command.get_keywords()
        entities = Entity.objects.filter(status__in=[-1, 0])
        exclude_keywords = ('宝宝', '婴儿', '枪', '硬币', 'C4')

        for entity in entities:
            for keyword in keywords:
                if keyword not in exclude_keywords and entity.title and keyword in entity.title:
                    entity.status = -1
                    entity.save()
                    self.stdout.write(u'{},{},{}'.format(keyword, entity.title, entity.id))

    @staticmethod
    def get_keywords():
        with open('data/keywords.txt') as f:
            keywords = [keyword.strip().decode('utf-8') for keyword in f]
            keywords = [keyword for keyword in keywords if keyword]
            return keywords
