from django.db import models
from django.core.cache import cache
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
import random
from datetime import datetime, timedelta

from django.utils.log import getLogger

log = getLogger('django')


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

    def guess(self, category_id=None, count=5):
        size = count * 50
        entity_list = self.new_or_selection(category_id=category_id)[:size]

        entities = random.sample(entity_list, count)
        return entities


class EntityLikeQuerySet(models.query.QuerySet):

    def popular(self, scale):
        dt = datetime.now()

        if scale == 'weekly':
            days = timedelta(days=7)
        else:
            days = timedelta(days=1)
        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        return self.filter(created_time__gte=popular_time).annotate(dcount=models.Count('entity')).values_list('entity_id', flat=True)

    def user_like_list(self, user, entity_list):

        return self.filter(entity_id__in=entity_list, user=user).values_list('entity_id', flat=True)


class EntityLikeManager(models.Manager):

    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)

    def popular(self, scale='weekly'):
        key = 'entity_popular_%s' % scale
        res = cache.get(key)
        # if scale == 'weekly':
        #     res = cache.get('entity_popular_weekly')
        # else:
        #     res = cache.get('entity_popular_daily')
        if res:
            return res
        res = self.get_query_set().popular(scale)
        cache.set(key, res, timeout=3600)
        return res

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

    def set_user_refresh_datetime(self, session):
        log.info(datetime.now())
        cache.set(session, datetime.now())

    def get_user_unread(self, session):
        refresh_datetime = cache.get(session)
        # log.info(type( refresh_datetime ))
        if refresh_datetime is None:
            return 0

        unread_count = self.published().filter(pub_time__range=(refresh_datetime, datetime.now() )).count()
        return unread_count

__author__ = 'edison'
