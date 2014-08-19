from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# import random





class EntityQuerySet(models.query.QuerySet):
    pass


class EntityManager(models.Manager):

    def get_query_set(self):
        return EntityQuerySet(self.model, using = self._db)


__author__ = 'edison'
