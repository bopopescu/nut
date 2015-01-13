from django.db import models
from django.utils.log import getLogger
from django.core.cache import cache

log = getLogger('django')


class CategoryManager(models.Manager):

    def toDict(self):
        res = []
        for c in self.all():

            _content = []
            for sc in c.sub_categories.filter(status__gte=0):
                r = {
                        'category_id':sc.id,
                        'category_title':sc.title,
                        'status':int(sc.status),
                        # 'category_icon_large':sc.icon_large_url,
                        # 'category_icon_small':sc.icon_small_url,
                }

                if sc.icon is not  None:
                    r['category_icon_large'] = sc.icon_large_url
                    r['category_icon_small'] = sc.icon_small_url
                _content.append(r)

            res.append({
                'group_id' : c.id,
                'title' : c.title,
                'status' : c.status,
                'category_count': c.sub_category_count,
                'content': _content,
            })
        return res

__author__ = 'edison'
