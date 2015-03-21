from apps.core.models import Entity, Buy_Link, Note, GKUser, Entity_Like
from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.utils.log import getLogger
import time
from hashlib import md5

log = getLogger('django')


class APIUser(GKUser):

    class Meta:
        proxy = True

    @property
    def fans_list(self):
        # log.info("cache cache")
        # return self.fans.all().values_list('follower_id', flat=True)
        key_string = "user_fans_%s" % self.id
        key = md5(key_string.encode('utf-8')).hexdigest()

        res = cache.get(key)
        if res:
            log.info("hit hit")
            return res
        res = super(APIUser, self).fans_list
        cache.set(key, res, timeout=3600)
        return res


    @property
    def following_list(self):
        # log.info("cache cache")
        key_string = "user_follow_%s" % self.id
        key = md5(key_string.encode('utf-8')).hexdigest()

        res = cache.get(key)
        if res:
            # log.info("hit hit")
            return res
        res = list(super(APIUser, self).following_list)
        cache.set(key, res, timeout=3600)
        return res


class APIEntity(Entity):
    class Meta:
        proxy = True


    @property
    def buy_links(self):
        return APIBuyLink.objects.filter(entity=self.id)

    def toDict(self):
        res = super(Entity, self).toDict()
        res['chief_image'] = self.chief_image
        res['detail_images'] = self.detail_images
        res['entity_id'] = self.id
        res['note_count'] = self.note_count
        res['like_count'] = self.like_count
        return res

    def v4_toDict(self, user_like_list=None):
        # log.info(user_like_list)
        res = self.toDict()
        res.pop('id', None)
        res.pop('images', None)
        res.pop('user_id', None)
        res.pop('rate', None)
        res['entity_id'] = self.id
        res['item_id_list'] = ['54c21867a2128a0711d970da']
        # res['price'] = "%s" % int(self.price)
        res['weight'] = 0
        res['score_count'] = 0
        res['mark_value'] = 0
        res['mark'] = "none"
        res['created_time'] = time.mktime(self.created_time.timetuple())
        res['updated_time'] = time.mktime(self.created_time.timetuple())
        # res['novus_time'] = time.mktime(self.created_time.timetuple())
        res['creator_id'] = self.user_id
        # res['old_root_category_id'] = 9
        # res['old_category_id'] = 152
        res['total_score'] = 0
        res['like_already'] = 0
        if user_like_list and self.id in user_like_list:
            res['like_already'] = 1

        res['item_list'] = list()
        for b in self.buy_links.all():
            res['item_list'].append(
                b.v4_toDict()
            )
        return res

    @property
    def likes(self):
        return super(APIEntity, self).likes


class APIBuyLink(Buy_Link):
    class Meta:
        proxy = True

    def v4_toDict(self):
        res = self.toDict()
        res.pop('link', None)
        res['buy_link'] = "http://h.guoku.com%s?type=mobile" % reverse('v4_visit_item', args=[self.origin_id])
        res['price'] = int(self.price)
        return res


class APINote(Note):
    class Meta:
        proxy = True

    def v4_toDict(self, user_note_pokes=None, has_entity=False):
        res = self.toDict()
        res.pop('note', None)
        res.pop('id', None)
        res.pop('status', None)
        res['note_id'] = self.id
        res['content'] = self.note
        res['comment_count'] = self.comment_count
        res['poke_count'] = self.poke_count
        res['created_time'] = time.mktime(self.post_time.timetuple())
        res['updated_time'] = time.mktime(self.updated_time.timetuple())
        res['creator'] = self.user.v3_toDict()
        res['is_selected'] = self.status
        res['poker_id_list'] = list(self.poke_list)
        # log.info(user_note_pokes)
        res['poke_already'] = 0
        if user_note_pokes and self.id in user_note_pokes:
            res['poke_already'] = 1

        if has_entity:
            res['brand'] = self.entity.brand
            res['title'] = self.entity.title
            res['chief_image'] = self.entity.chief_image
            res['category_id'] = self.entity.category_id

        return res



__author__ = 'edison'
