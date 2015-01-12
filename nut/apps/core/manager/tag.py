from django.db import models, connection
from django.db.models import Count
from apps.core.manager import dictfetchall
from django.core.cache import cache

class EntityTagQuerySet(models.query.QuerySet):

    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        # return self.raw('SELECT tag_id, core_tag.tag, count(tag_id) as tcount from core_entity_tag join core_tag on tag_id = core_tag.id where user_id =1 group by tag_id')

class EntityTagManager(models.Manager):
    cursor = connection.cursor()

    def get_queryset(self):
        return EntityTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):
        sql = "SELECT tag_id, core_tag.tag, count(tag_id) as tcount \
                  from core_entity_tag join core_tag on tag_id = core_tag.id \
                   where user_id=%s group by tag_id ORDER BY tcount DESC" % user

        self.cursor.execute(sql)

        return dictfetchall(self.cursor)
        # return self.raw("SELECT tag_id, core_tag.tag, count(tag_id) as tcount from core_entity_tag join core_tag on tag_id = core_tag.id where user_id =1 group by tag_id", translations=name_map)
        # return self.get_queryset().user_tags(user)


__author__ = 'edison'
