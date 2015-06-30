from django.db import models
from django.core.cache import cache

from datetime import datetime

from random import shuffle




class ArticleManager(models.Manager):
    def get_published_by_user(self,user):
        # publish = 2   because  Article.published = 2, user 2 to avoid circular reference
        return self.get_queryset().filter(publish=2, creator=user).order_by('-updated_datetime')

    def get_drafted_by_user(self,user):
        pass



class SelectionArticleManager(models.Manager):
    def get_related_cache_key(self, article):
        key = 'related_article_for_%s' % article.pk
        return key

    def article_related(self, article):
        '''
        get a list of selection article that related to the article passed in as param
        :param article: article to be related
        :return:  all selection article , pubed , related to the param article
        '''
        key = self.get_related_cache_key(article)
        related_list = cache.get(key)

        if related_list:
            return list(related_list)

        related_list = self.get_queryset()\
                            .filter(pub_time__lte = datetime.now())\
                            .exclude(article__pk=article.pk)\
                            .order_by('-pub_time')[:30]

        rList = list(related_list)
        shuffle(rList)
        # TODO: use longer timeout
        cache.set(key, rList ,timeout=10)
        return related_list




    def published_until(self, until_time):
        return self.get_queryset().filter(is_published=True)

