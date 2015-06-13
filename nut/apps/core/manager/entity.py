from django.db import models
from django.core.cache import cache
from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
import random
from datetime import datetime, timedelta

from django.utils.log import getLogger
from django.conf import settings


log = getLogger('django')

class EntityQuerySet(models.query.QuerySet):

    def selection(self):
        return self.filter(status=1)

    def new(self):
        return self.filter(status=0)

    def new_or_selection(self, category_id):
        if category_id:
            return self.using('slave').filter(category_id=category_id, status__gte=0)
        else:
            return self.using('slave').filter(status__gte=0)


class EntityManager(models.Manager):

    def get_query_set(self):
        return EntityQuerySet(self.model, using = self._db)

    def selection(self):
        return self.get_query_set().selection()

    def new(self):
        return self.get_query_set().new()

    def new_or_selection(self, category_id=None):
        return self.get_query_set().new_or_selection(category_id)

    def guess(self, category_id=None, count=5, exclude_id= None):
        size = count * 10
        if exclude_id:
            entity_list = self.new_or_selection(category_id=category_id).exclude(pk=exclude_id)
        else:
            entity_list = self.new_or_selection(category_id=category_id)

        entities = random.sample(entity_list[:size], count)
        return entities

    # def sort_with_list(self, category_id=None):
    #     Entity_Like.objects.using('slave').filter(entity__category = 10).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')

def  isTestEnv():
     return  (settings.DATABASES['default']['NAME'] == 'test')  or (hasattr(settings,'LOCAL_TEST_DB') and settings.LOCAL_TEST_DB)


class EntityLikeQuerySet(models.query.QuerySet):

    def popular(self, scale):
        dt = datetime.now()
        weekly_days = 7
        # local test db  has NOT enough entity like data
        # this is a temp workaround for local testing

        if isTestEnv():
            weekly_days =70

        if scale == 'weekly':
            days = timedelta(days=weekly_days)
        else:
            days = timedelta(days=1)

        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        if isTestEnv:
            return self.filter(created_time__gte=popular_time).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')[:200]

        user_innqs = get_user_model()._default_manager.filter(is_active__gt=0).values_list('id', flat=True)
        return self.filter(created_time__gte=popular_time, user_id__in=user_innqs).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')[:200]

    def user_like_list(self, user, entity_list):

        return self.filter(entity_id__in=entity_list, user=user).values_list('entity_id', flat=True)

    def sort_with_list(self, category_id):
        return self.using('slave').filter(entity__category = category_id).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')

class EntityLikeManager(models.Manager):

    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)

    def popular(self, scale='weekly'):
        key = 'entity_popular_%s' % scale
        res = cache.get(key)
        if res:
            return list(res)
        res = self.get_query_set().popular(scale)
        cache.set(key, res, timeout=86400)
        return list(res)

    def popular_random(self, scale='weekly'):
        key = 'entity_popular_random_%s' % scale
        # popular_list = self.popular()
        res = cache.get(key)
        log.info(res)
        if res:
            return res
        source = self.popular(scale)
        res = random.sample(source, 60)
        cache.set(key, res, timeout=3600)
        return res

    def user_like_list(self, user, entity_list):

        return self.get_query_set().user_like_list(user=user, entity_list=entity_list)

    def sort_with_list(self, category_id):

        entity_id_list = self.get_query_set().sort_with_list(category_id)

        return list(entity_id_list)



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
        # _key = "%s_selection" % session
        cache.set(session, datetime.now())

    def get_user_unread(self, session):
        # _key = "%s_selection" % session
        refresh_datetime = cache.get(session)
        log.info(type( refresh_datetime ))
        if refresh_datetime is None:
            return 0

        unread_count = self.published().filter(pub_time__range=(refresh_datetime, datetime.now())).count()
        # log.debug(unread_count.query)
        return unread_count

__author__ = 'edison'
