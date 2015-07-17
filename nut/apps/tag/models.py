from django.db import models, connection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from apps.core.models import BaseModel

from django.db.models import Count
from django.core.cache import cache

from django.utils.log import getLogger
# from apps.core.manager import dictfetchall
import random

log = getLogger('django')

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class ContentTagQuerySet(models.query.QuerySet):
    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        # self.raw()
        # return

    def popular(self):
        return self.annotate(tcount=Count('tag')).order_by('-tcount')[:300]


class ContentTagManager(models.Manager):

    def popular_entity_tag(self):
        key = 'new_entity_tag_popular_all'
        res = cache.get(key)
        if res:
            return list(res)

        res = self.get_queryset().popular()
        #TODO : make the timeout to 1 day
        cache.set(key, res , timeout=86400)
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
        cache.set(key, res , timeout=900)

        return res

    def get_queryset(self):
        return ContentTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):
        # obj = self.raw("SELECT tag_content_tags.id, tag_id, tag_tags.name, tag_tags.hash, count(tag_id) as entity_count \
        #           from tag_content_tags join tag_tags on tag_id = tag_tags.id \
        #            where creator_id=%s group by tag_id ORDER BY entity_count DESC" % user)
        obj = self.raw('SELECT id, tag_id, COUNT(tag_id) AS entity_count \
                        FROM tag_content_tags WHERE creator_id=%s GROUP BY tag_id ORDER BY entity_count DESC' % user)
        # c = connection.cursor()
        # sql = "SELECT tag_id, tag_tags.name, tag_tags.hash, count(tag_id) as entity_count \
        #           from tag_content_tags join tag_tags on tag_id = tag_tags.id \
        #            where creator_id=%s group by tag_id ORDER BY entity_count DESC" % user
        #
        # # log.info(sql)
        # c.execute(sql)
        # # try:
        # #     c.execute(sql)
        # # finally:
        # #     c.close()
        # res = dictfetchall(c)
        res = list()
        for row in obj:
            dict = {
                'tag_id': row.tag_id,
                'tag': row.tag.name,
                'tag_hash': row.tag.hash,
                'entity_count': row.entity_count,
            }
            print  dict
            res.append(dict)
            # print row.tag

        return res


class Tags(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    hash = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.BooleanField(default=False)
    image = models.URLField(max_length=255, null=True)

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    @property
    def tag_hash(self):
        return self.hash[:8]

    def get_absolute_url(self):
        return "/t/%s/" % self.tag_hash


class Content_Tags(BaseModel):
    tag = models.ForeignKey(Tags)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    target_content_type = models.ForeignKey(ContentType, related_name='tag_target', blank=True, null=True)
    target_object_id = models.BigIntegerField(null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, editable=True, db_index=True)
    # created_datetime = models.DateTimeField(db_index=True)

    objects = ContentTagManager()

    class Meta:
        unique_together = ('tag', 'creator', 'target_content_type', 'target_object_id')


__author__ = 'xiejiaxin'
