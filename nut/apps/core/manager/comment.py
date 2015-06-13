from django.db import models
from django.utils.log import getLogger

log = getLogger('django')


class CommentQuerySet(models.query.QuerySet):

    def normal(self):
        return self.exclude(user__is_active__lte=0)
    #
    # def top_or_normal(self):
    #     return self.filter(status__gte=0, user__is_active__gte=1)

class CommentManager(models.Manager):

    def get_query_set(self):
        return CommentQuerySet(self.model, using=self._db)

    def normal(self):
        return self.get_query_set().normal()

__author__ = 'edison'
