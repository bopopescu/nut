from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# import random
from datetime import datetime, timedelta


class EntityQuerySet(models.query.QuerySet):
    pass


class EntityManager(models.Manager):

    def get_query_set(self):
        return EntityQuerySet(self.model, using = self._db)



class EntityLikeQuerySet(models.query.QuerySet):


    def popular(self):
        dt = datetime.now()
        days = timedelta(days=7)
        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        return self.filter(created_time__gt=popular_time).annotate(dcount=models.Count('entity')).values_list('entity_id', flat=True)


class EntityLikeManager(models.Manager):

    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)


    def popular(self):
        return self.get_query_set().popular()

__author__ = 'edison'
