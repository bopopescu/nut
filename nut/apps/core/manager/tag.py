from django.db import models, connection
from django.db.models import Count
from django.core.cache import cache

from django.utils.log import getLogger
from apps.core.manager import dictfetchall


log = getLogger('django')


class EntityTagQuerySet(models.query.QuerySet):

    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        # return self.raw('SELECT tag_id, core_tag.tag, count(tag_id) as tcount from core_entity_tag join core_tag on tag_id = core_tag.id where user_id =1 group by tag_id')

class EntityTagManager(models.Manager):


    def get_queryset(self):
        return EntityTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):
        c = connection.cursor()
        sql = "SELECT tag_id, core_tag.tag, core_tag.tag_hash, count(tag_id) as tcount \
                  from core_entity_tag join core_tag on tag_id = core_tag.id \
                   where user_id=%s group by tag_id ORDER BY tcount DESC" % user

        # log.info(sql)
        c.execute(sql)
        # try:
        #     c.execute(sql)
        # finally:
        #     c.close()
        res = dictfetchall(c)
        return res


__author__ = 'edison'
