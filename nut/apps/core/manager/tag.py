from django.db import models
from django.db.models import Count


class EntityTagQuerySet(models.query.QuerySet):

    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')

class EntityTagManager(models.Manager):

    def get_queryset(self):
        return EntityTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):

        return self.get_queryset().user_tags(user)


__author__ = 'edison'
