from apps.core.models import Entity, Buy_Link, Note, \
    GKUser, Selection_Entity, Sina_Token, \
    Taobao_Token, WeChat_Token, User_Follow, Category

from apps.core.models import Selection_Article, Article
from apps.notifications.models import JpushToken
from apps.notifications import notify
# from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.utils.html import strip_tags


import time
from hashlib import md5

from apps.mobile.models import Session_Key

from django.conf import settings

imghost = getattr(settings, 'IMAGE_HOST')


from django.utils.log import getLogger
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

    def v4_toDict(self, visitor=None):

        key_string = "user_v3_%s" % self.id
        key = md5(key_string.encode('utf-8')).hexdigest()
        res = cache.get(key)
        if not res:
            res = self.toDict()
            res.pop('password', None)
            res.pop('last_login', None)
            res.pop('id', None)
            res.pop('date_joined', None)
            res.pop('is_admin', None)
            res.pop('is_superuser', None)

            res['user_id'] = self.id
            # res['is_active'] = self.active
            # res['is_censor'] = False

            try:
                res['nickname'] = self.profile.nickname
                res['bio'] = self.profile.bio
                res['gender'] = self.profile.gender
                res['location'] = self.profile.location
                res['city'] = self.profile.city
                res['website'] = self.profile.website
                res['avatar_large'] = self.profile.avatar_url
                res['avatar_small'] = self.profile.avatar_url

            # res['verified'] = self.profile.email_verified
                res['relation'] = 0
            except Exception, e:
                log.error("Error: user id %s %s", (self.id,e.message))
            cache.set(key, res, timeout=86400)

        res['like_count'] = self.like_count
        res['entity_note_count'] = self.post_note_count
        res['tag_count'] = self.tags_count
        res['fan_count'] = self.fans_count
        res['following_count'] = self.following_count

        try:
            res['sina_screen_name'] = self.weibo.screen_name
        except Sina_Token.DoesNotExist, e:
            log.info("info: %s" % e.message)

        try:
            res['taobao_nick'] = self.taobao.screen_name
            res['taobao_token_expires_in'] = self.taobao.expires_in
        except Taobao_Token.DoesNotExist, e:
            log.info("info: %s", e.message)

        if visitor:
            if self.id == visitor.id:
                res['relation'] = 4
            elif self.id in visitor.concren:
                res['relation'] = 3
            elif self.id in visitor.following_list:
                res['relation'] = 1
            elif self.id in visitor.fans_list:
                res['relation'] = 2
        return res


class APIUser_Follow(User_Follow):

    class Meta:
        proxy = True


class APIWeiboToken(Sina_Token):

    class Meta:
        proxy = True

    def v4_toDict(self):
        res = self.toDict()
        return res


class APIEntity(Entity):
    class Meta:
        proxy = True

    @property
    def buy_links(self):
        return APIBuyLink.objects.filter(entity=self.id)

    @property
    def notes(self):
        return APINote.objects.filter(entity=self)

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
        # res['item_id_list'] = ['54c21867a2128a0711d970da']
        # res['price'] = "%s" % int(self.price)
        # res['weight'] = 0
        # res['score_count'] = 0
        # res['mark_value'] = 0
        # res['mark'] = "none"
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
        res['buy_link'] = "http://api.guoku.com%s?type=mobile" % reverse('v4_visit_item', args=[self.origin_id])
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

    # def save(self, *args, **kwargs):
    #     super(self, APINote).save(*args, **kwargs)

class APISelection_Entity(Selection_Entity):

    class Meta:
        proxy = True


class APICategory(Category):

    class Meta:
        proxy = True

    def v4_toDict(self):
        res = self.toDict()
        res.pop('cover')
        res.update(
            {'cover_url': self.cover_url}
        )
        return res


class APIWeChatToken(WeChat_Token):

    class Meta:
        proxy = True

    def __unicode__(self):
        return self.unionid

# TODO Selection Articles

class APISeletion_Articles(Selection_Article):

    class Meta:
        proxy = True

    @property
    def api_article(self):
        return  APIArticle.objects.get(pk=self.article_id)
        # return APIArticle(self.article)


import HTMLParser
h_parser = HTMLParser.HTMLParser()
class APIArticle(Article):

    class Meta:
        proxy = True

    @property
    def strip_tags_content(self):
        return h_parser.unescape(strip_tags(self.content))

    def v4_toDict(self):
        res = self.toDict()
        res.pop('id', None)
        res.pop('creator_id')
        res.pop('created_datetime', None)
        res.pop('updated_datetime', None)
        res['article_id'] = self.id
        res['tags'] = self.tag_list
        res['content'] = self.strip_tags_content
        res['url'] = self.get_absolute_url()
        res['creator'] = self.creator.v3_toDict()
        return res


# TODO API JPUSH
class APIJpush(JpushToken):

    class Meta:
        proxy = True


# TODO API Seseion
class APISession_Key(Session_Key):

    class Meta:
        proxy = True


def remove_jpush_register_id(sender, instance, **kwargs):

    if issubclass(sender, APISession_Key):
        _user = instance.user
        log.info(_user)

post_delete.connect(remove_jpush_register_id, sender=APISession_Key, dispatch_uid="user_logout_remove_jpush_id")


def user_follow_notification(sender, instance, created, **kwargs):
    if issubclass(sender, APIUser_Follow) and created:
        # log.info(instance)
        notify.send(instance.follower, recipient=instance.followee, verb=u'has followed you', action_object=instance, target=instance.followee)

post_save.connect(user_follow_notification, sender=APIUser_Follow, dispatch_uid="user_follow_notification")

__author__ = 'edison'
