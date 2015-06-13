from django.db import models, connection
from django.db.models import Count
from django.core.cache import cache

from django.utils.log import getLogger
from apps.core.manager import dictfetchall
import random

log = getLogger('django')


class EntityTagQuerySet(models.query.QuerySet):

    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')

        # return self.raw('SELECT tag_id, core_tag.tag, count(tag_id) as tcount from core_entity_tag join core_tag on tag_id = core_tag.id where user_id =1 group by tag_id')
    def popular(self):
        return self.annotate(tcount=Count('tag')).order_by('-tcount')[:300]

class EntityTagManager(models.Manager):

    def popular_entity_tag(self):
        key = 'new_entity_tag_popular_all'
        res = cache.get(key)
        if res:
            return list(res)

        res = self.get_queryset().popular()
        #TODO : make the timeout to 1 day
        cache.set(key, res , timeout=100)
        return res


    def popular_random(self, tag_count=15):
        key = 'new_entity_tag_popular_random_%s' % tag_count
        res = cache.get(key)
        log.info(res)
        if res:
            return res

        popularTags = self.popular_entity_tag()
        if popularTags.count  < tag_count:
            res =  popularTags;
        else:
            res =  random.sample(popularTags, tag_count)
        #TODO: make the timeout to 15 minute
        cache.set(key, res , timeout=100)

        return res


    def get_queryset(self):
        return EntityTagQuerySet(self.model, using = self._db)


    def user_tags(self, user):
        c = connection.cursor()
        sql = "SELECT tag_id, core_tag.tag, core_tag.tag_hash, count(tag_id) as entity_count \
                  from core_entity_tag join core_tag on tag_id = core_tag.id \
                   where user_id=%s group by tag_id ORDER BY entity_count DESC" % user

        # log.info(sql)
        c.execute(sql)
        # try:
        #     c.execute(sql)
        # finally:
        #     c.close()
        res = dictfetchall(c)
        return res

    def tags(self, tag_id_list):
        key_string = ','.join(str(s) for s in tag_id_list)
        c = connection.cursor()
        sql = "SELECT tag_id, core_tag.tag, core_tag.tag_hash, count(tag_id) as entity_count \
                  from core_entity_tag join core_tag on tag_id = core_tag.id \
                   where tag_id in (%s) group by tag_id ORDER BY entity_count DESC" % key_string

        # log.info(sql)
        c.execute(sql)
        # try:
        #     c.execute(sql)
        # finally:
        #     c.close()
        res = dictfetchall(c)
        return res



__author__ = 'edison'
