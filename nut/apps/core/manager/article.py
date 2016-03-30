from django.db import models
from django.core.cache import cache
from datetime import datetime, timedelta
from random import shuffle

from django.core.paginator import  Paginator,InvalidPage
from django.contrib.auth import get_user_model
from django.utils.log import getLogger
from django.db.models import Count

import random
log = getLogger('django')


class ArticleDigQuerySet(models.query.QuerySet):
    def popular(self, scale):
        dt = datetime.now()
        weekly_days = 7
        if scale == 'weekly':
            days = timedelta(days = weekly_days)
        else:
            days = timedelta(days=1)

        popular_time = (dt-days).strftime("%Y-%m-%d") + ' 00:00'
        user_innqs = get_user_model()._default_manager.filter(is_active__gt=0)\
                                                      .values_list('id', flat=True)
        return self.filter(created_time__gte=popular_time,user_id__in=user_innqs)\
                   .values_list('article',flat=True)\
                   .annotate(dcount=Count('aritlce'))\
                   .order_by('-dcount')[:400]

    def user_dig_list(self, user, article_list):
        return self.filter(article_id__in=article_list, user=user)\
                   .values_list('article_id', flat=True)


class ArticleDigManager(models.Manager):
    def get_queryset(self):
        return ArticleDigQuerySet(self.model, using=self._db)

    def user_dig_list(self, user, article_list):
        return self.get_queryset().user_dig_list(user, article_list)

    def popular(self, scale='weekly'):
        key = 'article:popular:%s' % scale
        res = cache.get(key)
        if res:
            return list(res)
        else:
            res = self.get_queryset().popular(scale)
            cache.set(key, res, timeout=3600*24)
            return res

    def popular_random(self, scale='weekly'):
        key  ='article:popular:random:%s' %scale
        res = cache.get(key)
        if res:
            return res
        else:
            source = self.popular(scale)
            out_count= 60
            try :
                res = random.sample(source, out_count)
                cache.set(key, res, timeout=3600*24)
            except ValueError:
                res = source
            return res

class ArticleManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(publish=2).order_by('-created_datetime')

    def get_published_by_user(self,user):
        # publish = 2   because  Article.published = 2, user 2 to avoid circular reference
        return self.get_queryset().using('slave').filter(publish=2, creator=user).order_by('-created_datetime')

    def get_drafted_by_user(self,user):
        return self.get_queryset().using('slave').filter(publish=1, creator=user).order_by('-updated_datetime')

    def get_removed_by_user(self,user):
        return self.get_queryset().using('slave').filter(publish=0, creator=user).order_by('-updated_datetime')


class SelectionArticleQuerySet(models.query.QuerySet):
    def discover(self):
        start_date = datetime.now()
        end_date = start_date - timedelta(days=3)
        return self.using('slave').filter(is_published=True, pub_time__range=(end_date, start_date)).order_by('-article__read_count')

    def published_from(self, from_time=None):
        if from_time is None:
            from_time = datetime.now()-timedelta(days=30)

        return self.using('slave')\
                   .select_related('article')\
                   .filter(is_published=True, pub_time__lte=datetime.now(), pub_time__gte=from_time)\
                   .order_by('-article__read_count')


class SelectionArticleManager(models.Manager):

    def get_queryset(self):
        return SelectionArticleQuerySet(self.model)

    def discover(self):
        return self.get_queryset().discover()

    def get_popular(self):
        #  article in recent week 50%
        #  most read article in recent month 50%
        #  combine them together
        #  shuffle the list
        key = self.get_popular_cache_key()
        merged =  cache.get(key)
        if merged:
            return merged
        # most read article
        # most recent article
        last_month = datetime.now() - timedelta(days=14)
        last_week =  datetime.now() - timedelta(days=7)

        pop_articles = list(self.published_from(from_time=last_month).order_by('-article__read_count')[:16])
        recent_articles = list(self.published_from(from_time=last_week)[:4])
        merged = list(set(pop_articles + recent_articles))
        shuffle(merged)
        #set cache timeout longer to 6 hour
        cache.set(key , merged, timeout=6*3600)
        return merged


    def get_popular_cache_key(self):
        key = 'popular_article_list'
        return key

    def get_related_cache_key(self, article):
        key = 'related_article_for_%s' % article.pk
        return key


    def published(self,until_time=None):
        return self.published_until()

    def published_by_user(self,user):
        return self.published_until().filter(article__creator = user)

    def pending(self):
        return self.get_queryset().filter(is_published=False)

    def published_until(self,until_time=None):
        if until_time is None:
            until_time = datetime.now()
        return self.get_queryset().select_related('article').using('slave').filter(is_published=True, pub_time__lte=until_time).order_by('-pub_time')

    def published_from(self, from_time=None):
        if from_time is None:
             from_time = datetime.now() - timedelta(days=30)
        return self.get_queryset().using('slave').published_from(from_time=from_time)

    def article_related(self, article, request_page=1):
        '''
        get a list of selection article that related to the article passed in as param
        :param article: article to be related
        :return:  all selection article , pubed , related to the param article
        '''
        article_per_page = 6
        key = self.get_related_cache_key(article)
        related_list = cache.get(key)

        if not related_list:
            related_list = self.published()\
                           .exclude(article__pk=article.pk)\
                           .order_by('-pub_time')[:100]
            cache.set(key, related_list, 6*3600)

        # shuffle(related_list)
        p = Paginator(related_list, article_per_page)
        res = None
        try:
            res = p.page(request_page)
        except InvalidPage as e :
            log.info('can not fetch related article form paginator')
            return None
        return res

