from django.db import models
from django.utils.log import getLogger

log = getLogger('django')


class NoteQuerySet(models.query.QuerySet):

    def normal(self):
        return self.filter(status=0, user__is_active__gte=1)


class NoteManager(models.Manager):

    def get_query_set(self):
        return NoteQuerySet(self.model, using = self._db)

    def normal(self):
        return self.get_query_set().normal()


class NotePokeQuerySet(models.query.QuerySet):

    def user_poke_list(self, user, note_list):
        return self.filter(user=user, note_id__in=note_list).values_list('note_id', flat=True)

class NotePokeManager(models.Manager):

    def get_queryset(self):
        return NotePokeQuerySet(self.model, using=self._db)

    def user_poke_list(self, user, note_list):
        # log.info(note_list)
        return  self.get_queryset().user_poke_list(user, note_list)

__author__ = 'edison7500'
