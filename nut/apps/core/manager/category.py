from django.db import models
from django.db.models import Count
from django.utils.log import getLogger

from apps.core.manager import get_entity_model, get_entity_like_model
# from apps.core.models import Entity_Like
from django.core.cache import cache
from hashlib import md5
import random

log = getLogger('django')

class CategoryQuerySet(models.query.QuerySet):

    def popular(self):
        popular_list = get_entity_like_model().objects.popular()
        gids = get_entity_model().objects.filter(pk__in=popular_list).values_list('category__group', flat=True).annotate(dcount=Count('category__group')).order_by('-dcount')
        return gids

class CategoryManager(models.Manager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def toDict(self):

        res = []
        for c in self.all():

            _content = []
            for sc in c.sub_categories.filter(status__gte=0):

                title = sc.title
                if '+' in title:
                    title = c.title
                r = {
                        'category_id':sc.id,
                        'category_title':title,
                        'status':int(sc.status),
                        # 'category_icon_large': None,
                        # 'category_icon_small':None,
                }

                if sc.icon is not  None:
                    r['category_icon_large'] = sc.icon_large_url
                    r['category_icon_small'] = sc.icon_small_url
                _content.append(r)

            res.append({
                'group_id' : c.id,
                'title' : c.title,
                'status' : int(c.status),
                'category_count': c.sub_category_count,
                'content': _content,
            })
        return res

    def popular(self):
        key = "group:popular"
        gids = cache.get(key)
        if gids is None:
            gids = self.get_queryset().popular()
            cache.set(key, gids, timeout=86400)

        res = []
        for gid in gids:
            r = self.get(pk = gid)
            res.append(r)
        return res

class SubCategoryQuerySet(models.query.QuerySet):

    def map(self, group_id_list):
        return self.filter(group_id__in=group_id_list).values_list('id', flat=True)

    def popular(self):
        popular_list = get_entity_like_model().objects.popular()
        cids = get_entity_model().objects.filter(pk__in=popular_list).annotate(dcount=Count('category')).values_list('category_id', flat=True)
        return self.filter(id__in=list(cids), status=True)


class SubCategoryManager(models.Manager):

    def get_queryset(self):
        return SubCategoryQuerySet(self.model, using=self._db)

    def map(self, group_id_list):
        key_string = ''.join(str(s) for s in group_id_list)
        key = md5(key_string.encode('utf-8')).hexdigest()
        res = cache.get(key)
        if res:
            return res

        res = self.get_queryset().map(group_id_list)
        cache.set(key, res, timeout=86400)
        return res

    def popular(self):
        return self.get_queryset().popular()

    def popular_random(self, total=20):
        key = "entity:category:popular"
        # key = md5(key_string.encode('utf-8')).hexdigest()
        res = cache.get(key)
        if res:
            return res

        if self.popular().count() < total :
            return self.popular()

        res = random.sample(self.popular(), total)
        cache.set(key, res, timeout=3600)
        return res

__author__ = 'edison'
