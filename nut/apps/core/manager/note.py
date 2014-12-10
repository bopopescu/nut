from django.db import models


class NoteQuerySet(models.query.QuerySet):

    def normal(self):
        return self.filter(status=0)


class NoteManager(models.Manager):

    def get_query_set(self):
        return NoteQuerySet(self.model, using = self._db)

    def normal(self):
        return self.get_query_set().normal()


__author__ = 'edison7500'
