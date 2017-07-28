# coding=utf-8

from django.core.management.base import BaseCommand

from apps.core.models import GKUser, Note, Entity, Article_Remark


class Command(BaseCommand):
    help = 'clean all blocked user\'s data'

    def handle(self, *args, **options):
        notes = Note.objects.filter(user__is_active=GKUser.remove).exclude(status=Note.remove)
        delete_note_amount = notes.update(status=Note.remove)
        self.stdout.write('Delete {} notes.'.format(delete_note_amount))

        entities = Entity.objects.filter(user__is_active=GKUser.remove).exclude(status=Entity.remove)
        delete_entity_amount = entities.update(status=Entity.remove)
        self.stdout.write('Delete {} entities.'.format(delete_entity_amount))

        remarks = Article_Remark.objects.filter(user__is_active=GKUser.remove).exclude(status=Article_Remark.remove)
        delete_remark_amount = remarks.update(status=Article_Remark.remove)
        self.stdout.write('Delete {} entities.'.format(delete_remark_amount))
