from django.db import models
from django.core.cache import cache
from datetime import datetime, timedelta
from random import shuffle
from django.core.paginator import  Paginator,InvalidPage

from django.utils.log import getLogger
log = getLogger('django')


class ArticleManager(models.Manager):
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
        return self.filter(is_published=True, pub_time__range=(end_date, start_date)).order_by('-article__read_count')


class SelectionArticleManager(models.Manager):

    def get_queryset(self):
        return SelectionArticleQuerySet(self.model, using=self._db)

    def discover(self):
        return self.get_queryset().discover()

    def get_popular(self):
        key = self.get_popular_cache_key()
        merged =  cache.get(key)
        if merged:
            return merged
        # most read article
        # most recent article
        pop_articles = list(self.published().order_by('-article__read_count')[:8])
        recent_articles = list(self.published()[:16])
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
        return self.get_queryset().filter(is_published=False).using('slave')

    def published_until(self,until_time=None):
        if until_time is None:
            until_time = datetime.now()
        return self.get_queryset().select_related('article').filter(is_published=True, pub_time__lte=until_time).order_by('-pub_time')


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

