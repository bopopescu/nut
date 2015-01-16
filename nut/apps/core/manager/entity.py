from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# import random
from datetime import datetime, timedelta


class EntityQuerySet(models.query.QuerySet):

    def selection(self):
        return self.filter(status=1)

    def new(self):
        return self.filter(status=0)

    def new_or_selection(self, category_id):
        if category_id:
            return self.filter(category_id=category_id, status__gte=0)
        else:
            return self.filter(status__gte=0)


class EntityManager(models.Manager):

    def get_query_set(self):
        return EntityQuerySet(self.model, using = self._db)

    def selection(self):
        return self.get_query_set().selection()

    def new(self):
        return self.get_query_set().new()

    def new_or_selection(self, category_id=None):
        return self.get_query_set().new_or_selection(category_id)


class EntityLikeQuerySet(models.query.QuerySet):

    def popular(self):
        dt = datetime.now()
        days = timedelta(days=7)
        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        return self.filter(created_time__gt=popular_time).annotate(dcount=models.Count('entity')).values_list('entity_id', flat=True)

    def user_like_list(self, user, entity_list):

        return self.filter(entity_id__in=entity_list, user=user).values_list('entity_id', flat=True)


class EntityLikeManager(models.Manager):

    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_query_set().popular()

    def user_like_list(self, user, entity_list):

        return self.get_query_set().user_like_list(user=user, entity_list=entity_list)


class SelectionEntityQuerySet(models.query.QuerySet):

    def published(self):
        return self.filter(is_published=True)

    def pending(self):
        return self.filter(is_published=False)

class SelectionEntityManager(models.Manager):

    def get_queryset(self):
        return SelectionEntityQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def pending(self):
        return self.get_queryset().pending()

__author__ = 'edison'
