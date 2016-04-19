import random

from django.db import models
from django.db.models import Count
from django.conf import settings
from django.core.cache import cache
from django.utils.log import getLogger
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


log = getLogger('django')


class EntityQuerySet(models.query.QuerySet):
    def selection(self):
        return self.filter(status=1)

    def new(self):
        return self.filter(status=0)

    def active(self):
        return self.using('slave').filter(status__gte=-1)

    def new_or_selection(self, category_id):
        if isinstance(category_id, int) or isinstance(category_id ,str):
            return self.using('slave').filter(category_id=category_id,
                                              status__gte=0)

        elif isinstance(category_id, list):
            return self.using('slave').filter(category_id__in=category_id,
                                              status__gte=0)

        else:
            return self.using('slave').filter(status__gte=0)



    def sort(self, category_id, like=False):
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if like:
            return self.new_or_selection(category_id).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2) \
                .annotate(lnumber=Count('likes')) \
                .order_by('-lnumber')
        else:
            return self.new_or_selection(category_id).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2).distinct() \
                .order_by('-selection_entity__pub_time')


            # self.using('slave').filter(status=Entity.selection, selection_entity__pub_time__lte=_refresh_datetime, category=category_id)\
            # .order_by('-selection_entity__pub_time').filter(buy_links__status=2)
            # def get(self, *args, **kwargs):
            # # print kwargs, args
            # return super(EntityQuerySet, self).get(*args, **kwargs)

    def sort_group(self, category_ids, like=False):
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        like_key = 'entity:list:sort:like'

        if like:
            like_list = cache.get(like_key)
            if like_list:
                return like_list
            else:
                like_list = self.new_or_selection(category_ids).filter(
                    selection_entity__pub_time__lte=_refresh_datetime,
                    buy_links__status=2) \
                    .annotate(lnumber=Count('likes')) \
                    .order_by('-lnumber')
                cache.set(like_key, like_list, timeout=3600*24)
                return like_list
        else:
            return self.new_or_selection(category_ids).filter(
                selection_entity__pub_time__lte=_refresh_datetime,
                buy_links__status=2).distinct() \
                .order_by('-selection_entity__pub_time')


class EntityManager(models.Manager):
    # entity status: new:0,selection:1
    # get the current seller's selection entities and order by created-time.
    def get_published_by_seller(self,seller):
        return self.get_query_set().using('slave').filter(status=1, user=seller).order_by('-created_time')

    def get_user_added_entities(self, seller):
        return self.get_read_queryset().filter(status__gte=-1, user=seller).order_by('-created_time')

    def get_read_queryset(self):
        return EntityQuerySet(self.model).using('slave')

    def get_query_set(self):
        return EntityQuerySet(self.model, using=self._db)

    # def get(self, *args, **kwargs):
    # # print  kwargs
    #
    # entity_hash = kwargs['entity_hash']
    # key = 'entity:%s' % entity_hash
    # # print key
    # res = cache.get(key)
    # if res:
    #         print "hit cache", type(res)
    #         return res
    #     else:
    #         print "miss cache"
    #         res = self.get_query_set().get(*args, **kwargs)
    #         # key = 'entity:%s' % entity_hash
    #         cache.set(key, res, timeout=86400)
    #         return res
    def active(self):
        return self.get_queryset().active()

    def selection(self):
        return self.get_query_set().selection()

    def new(self):
        return self.get_query_set().new()

    def new_or_selection(self, category_id=None):
        return self.get_query_set().new_or_selection(category_id)

    def sort(self, category_id, like=False):
        assert category_id is not None
        return self.get_query_set().sort(category_id, like)

    def sort_group(self, category_ids, like=False):
        assert category_ids is not None
        return self.get_query_set().sort_group(category_ids, like)

    def guess(self, category_id=None, count=5, exclude_id=None):
        size = count * 10
        if exclude_id:
            entity_list = self.new_or_selection(
                category_id=category_id).exclude(pk=exclude_id).filter(
                buy_links__status=2)
        else:
            entity_list = self.new_or_selection(
                category_id=category_id).filter(buy_links__status=2)
        try:
            entities = random.sample(entity_list[:size], count)
        except ValueError:
            entities = entity_list[:count]
        return entities

        # def sort_with_list(self, category_id=None):
        #     Entity_Like.objects.using('slave').filter(entity__category = 10).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')


def isTestEnv():
    return (settings.DATABASES['default']['NAME'] == 'test') or (
        hasattr(settings, 'LOCAL_TEST_DB') and settings.LOCAL_TEST_DB)


class EntityLikeQuerySet(models.query.QuerySet):
    def popular(self, scale):
        dt = datetime.now()
        weekly_days = 7
        monthly_days = 30
        # local test db  has NOT enough entity like data
        # this is a temp workaround for local testing

        if isTestEnv():
            weekly_days = 7
        if scale == 'weekly':
            days = timedelta(days=weekly_days)
        elif scale == 'monthly':
            days = timedelta(days=monthly_days)
        else:
            days = timedelta(days=1)

        popular_time = (dt - days).strftime("%Y-%m-%d") + ' 00:00'
        if isTestEnv:
            return self.filter(created_time__gte=popular_time).values_list(
                'entity', flat=True).annotate(
                dcount=models.Count('entity')).order_by('-dcount')[:400]

        user_innqs = get_user_model()._default_manager.filter(
            is_active__gt=0).values_list('id', flat=True)
        return self.filter(created_time__gte=popular_time,
                           user_id__in=user_innqs).values_list('entity',
                                                               flat=True).annotate(
            dcount=models.Count('entity')).order_by('-dcount')[:400]

    def user_like_list(self, user, entity_list):

        return self.filter(entity_id__in=entity_list, user=user).values_list(
            'entity_id', flat=True)

        # def sort_with_list(self, category_id):
        # return self.using('slave').filter(entity__category = category_id).values_list('entity', flat=True).annotate(dcount=models.Count('entity')).order_by('-dcount')

class EntityLikeManager(models.Manager):
    def get_query_set(self):
        return EntityLikeQuerySet(self.model, using=self._db)

    def user_likes_id_list(self, user):
        return self.get_queryset().using('slave').filter(user=user)

    def active_entity_likes(self):
        #TODO: maybe filter out some deactived user's like ?
        return self.get_queryset().filter(entity__status__gte=-1)

    def popular(self, scale='weekly'):
        key = 'entity:popular:%s' % scale
        res = cache.get(key)
        if res:
            return list(res)
        res = self.get_query_set().popular(scale)
        cache.set(key, res, timeout=86400)
        return list(res)

    def popular_random(self, scale='weekly', out_count=60):
        key = 'entity:popular:random:%s' % scale
        # popular_list = self.popular()
        res = cache.get(key)
        log.info(res)
        if res:
            return res
        source = self.popular(scale)
        if isTestEnv():
            out_count = 6
        try:
            res = random.sample(source, out_count)
            cache.set(key, res, timeout=10800)
        except ValueError:
            res = source
        return res

    def user_like_list(self, user, entity_list):

        return self.get_query_set().user_like_list(user=user,
                                                   entity_list=entity_list)


class SelectionEntityQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def pending(self):
        return self.filter(is_published=False).exclude(
            entity__status__lt=1,
            entity__buy_links__status__in=(0, 1))

    def pending_and_removed(self):
        return self.filter(is_published=False,
                           entity__buy_links__status__in=(0, 1),
                           entity__status__lt=1)


class SelectionEntityManager(models.Manager):
    def get_queryset(self):
        return SelectionEntityQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def published_until(self, refresh_time=datetime.now()):
        return self.published().filter(pub_time__lte=refresh_time)

    def published_until_now(self, util_time=None):
        if util_time is None:
            util_time = datetime.now()
        return self.published().filter(pub_time__lte=util_time)

    def pending(self):
        return self.get_queryset().pending()

    def pending_and_removed(self):
        return self.get_queryset().pending_and_removed()

    def set_user_refresh_datetime(self, session, refresh_datetime=datetime.now()):
        log.info(refresh_datetime)
        # _key = "%s_selection" % session
        cache.set(session, refresh_datetime, timeout=8640000)

    def get_user_unread(self, session):
        # _key = "%s_selection" % session
        refresh_datetime = cache.get(session)
        log.info(refresh_datetime)
        if refresh_datetime is None:
            return 0

        unread_count = self.published().filter(
            pub_time__range=(refresh_datetime, datetime.now())).count()
        # log.debug(unread_count.query)
        return unread_count

    def category_sort_like(self, category_ids):
        # return self.get_queryset().published().filter(entity__category__in=category_ids).annotate(lnumber=Count('entity__likes')).order_by('-lnumber')
        res = self.published().filter(
            entity__category__in=category_ids).annotate(
            lnumber=Count('entity__likes')).order_by('-lnumber')
        # print res.query
        return res


__author__ = 'edison'
