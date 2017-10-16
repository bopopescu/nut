# coding=utf-8
from __future__ import print_function

from django.core.management.base import BaseCommand

from apps.core.models import Note


class Command(BaseCommand):
    def handle(self, *args, **options):
        keywords = Command.get_keywords()
        notes = Note.objects.filter(status=0, entity__status__gte=0)
        exclude_keywords = ('宝宝', '婴儿', '枪', '硬币', 'C4')

        for note in notes:
            for keyword in keywords:
                if keyword not in exclude_keywords and note.note and keyword in note.note:
                    note.status = Note.remove
                    note.save()
                    self.stdout.write(u'{},{},{}'.format(keyword, note.note, note.id))

    @staticmethod
    def get_keywords():
        with open('data/keywords.txt') as f:
            keywords = [keyword.strip().decode('utf-8') for keyword in f]
            keywords = [keyword for keyword in keywords if keyword]
            return keywords
