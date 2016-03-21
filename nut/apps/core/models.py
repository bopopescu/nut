# coding=utf-8

import time
import requests
import HTMLParser

from hashlib import md5
from datetime import datetime
from django.core import serializers
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group

from apps.notifications import notify
from apps.core.utils.image import HandleImage
from apps.core.utils.articlecontent import contentBleacher
from apps.core.extend.fields.listfield import ListObjectField
from apps.web.utils.datatools import get_entity_list_from_article_content
from apps.core.manager import *
from apps.core.manager.account import  AuthorizedUserManager
from haystack.query import SearchQuerySet



log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)

# if define avatar_host , then use avata_host , for local development .
avatar_host = getattr(settings, 'AVATAR_HOST', image_host)

feed_img_counter_host =  getattr(settings, 'IMG_COUNTER_HOST' , None)

class BaseModel(models.Model):
    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            # log.info( getattr(self, attr) )
            value = getattr(self, attr)
            if value is None:
                continue
            # log.info(value)
            d[attr] = "%s" % getattr(self, attr)
        # log.info(d)
        return d

    def pickToDict(self, *args):
        '''
          only work on simple python value fields ,
          can not use to serialize object field!
        '''
        d = {}
        for key in args:
            d[key] = getattr(self, key, None)
        return d


class GKUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    (remove, blocked, active, editor, writer) = (-1, 0, 1, 2, 3)
    USER_STATUS_CHOICES = [
        (writer, _("writer")),
        (editor, _("editor")),
        (active, _("active")),
        (blocked, _("blocked")),
        (remove, _("remove")),
    ]
    email = models.EmailField(max_length=255, unique=True)
    # is_active = models.BooleanField(_('active'), default=True)
    is_active = models.IntegerField(choices=USER_STATUS_CHOICES, default=active)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now())

    objects = GKUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['date_joined']

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.profile.nickname

    def has_guoku_assigned_email(self):
        return ('@guoku.com' in self.email ) and (len(self.email) > 29)

    @property
    def need_verify_mail(self):
        return (not self.profile.email_verified ) and (not self.need_change_mail)

    @property
    def need_change_mail(self):
        return ('@guoku.com' in self.email ) and (len(self.email) > 29)

    @property
    def has_published_article(self):
        count = self.articles.filter(publish=True).count()
        return count > 0

    @property
    def can_write(self):
        return self.is_writer or self.is_editor or self.is_staff

    @property
    def is_seller(self):
        return hasattr(self, 'seller_profile')

    @property
    def is_writer(self):
        return self.is_active == GKUser.writer

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_editor(self):
        return self.is_active == GKUser.editor

    @property
    def is_chief_editor(self):
        return self.is_admin

    @property
    def is_blocked(self):
        if self.is_active == GKUser.blocked or self.is_active == GKUser.remove:
            return True
        return False

    @property
    def not_blocked(self):
        return not self.is_blocked

    @property
    def is_removed(self):
        if self.is_active == GKUser.remove:
            return True
        return False

    @property
    def is_verified(self):
        return self.profile.email_verified

    # @property
    # def digged_articles(self):
    #     return self.digs

    @property
    def published_articles(self):
        return self.articles.filter(publish=Article.published)

    @property
    def drafting_articles(self):
        return self.articles.filter(published=Article.draft)

    @property
    def published_article_count(self):
        return self.articles.filter(publish=Article.published).count()

    @property
    def draft_article_count(self):
        return self.articles.filter(publish=Article.draft).count()

    @property
    def absolute_url(self):
        return reverse('web_user_index' , args=[self.pk])

    @property
    def mobile_url(self):
        return 'guoku://user/' + str(self.id) + '/'

    @property
    def like_count(self):
        key = 'user:like:%s' % self.pk
        res = cache.get(key)
        if res:
            log.info('user like count hit')
            return res
        else:
            log.info('user like count miss')
            res = self.likes.count()
            cache.set(key, res)
            return res

    def get_user_dig_key(self):
        return 'user:dig:%s' % self.pk

    @property
    def dig_count(self):
        key = self.get_user_dig_key()
        res = cache.get(key)
        if res:
            return res
        else:
            res = self.digs.count()
            cache.set(key, res)
            return res

    def incr_dig(self):
        key = self.get_user_dig_key()
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key,self.digs.count())

    def decr_dig(self):
        key = self.get_user_dig_key()
        try:
            cache.decr(key)
        except :
            cache.set(key, self.digs.count())

    def incr_like(self):
        key = 'user:like:%s', self.pk
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, self.likes.count())

    def decr_like(self):
        key = 'user:like:%s' % self.pk
        if self.likes.count() > 0:
            cache.decr(key)

    @property
    def create_entity_count(self):
        return self.entities.count()

    @property
    def post_note_count(self):
        return self.note.count()

    @property
    def post_note_comment_count(self):
        return self.note_comment.count()

    @property
    def tags_count(self):
        t = self.user_tags.values('tag').annotate(tcount=Count('tag'))
        return len(t)

    @property
    def article_count(self):
        return self.articles.count()

    @property
    def following_list(self):
        return self.followings.all().values_list('followee_id', flat=True)

    @property
    def fans_list(self):
        return self.fans.all().values_list('follower_id', flat=True)

    @property
    def concren(self):
        return list(set(self.following_list) & set(self.fans_list))

    @property
    def following_count(self):
        return self.followings.count()

    @property
    def fans_count(self):
        return self.fans.count()

    @property
    def bio(self):
        if hasattr(self, 'profile'):
            if self.profile.bio:
                return self.profile.bio
        return ''

    @property
    def nickname(self):
        if hasattr(self, 'profile'):
            if self.profile.nickname:
                return self.profile.nickname
        return ''

    @property
    def entity_liked_categories(self):
        _category_id_list = Entity_Like.objects.select_related('entity__category__group')\
                            .filter(user=self, entity__status__gte=Entity.freeze)\
                            .annotate(category_count=Count('entity__category__group'))\
                            .values_list('entity__category__group', flat=True)

        _category_list = Category.objects.filter(pk__in=_category_id_list)
        return set(_category_list)

    @property
    def recent_likes(self):
        rlikes = Entity_Like.objects.active_entity_likes().filter(user=self).order_by()
        return rlikes[:3]


    @property
    def avatar_url(self):
        if hasattr(self, 'profile'):
            return self.profile.avatar_url
        return "%s%s" % (settings.STATIC_URL, 'images/avatar/man.png')

    def set_admin(self):
        self.is_admin = True
        self.save()

    def v3_toDict(self, visitor=None):
        key = "user:v3:%s" % self.id
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
            res['is_censor'] = False

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
                log.error("Error: user id %s %s", (self.id, e.message))
            cache.set(key, res, timeout=86400)

        res['mail_verified'] = self.profile.email_verified
        res['like_count'] = self.like_count
        res['entity_note_count'] = self.post_note_count
        res['tag_count'] = self.tags_count
        res['dig_count'] = self.dig_count
        res['fan_count'] = self.fans_count
        res['following_count'] = self.following_count
        res['authorized_author'] = self.is_authorized_author

        try:
            res['sina_screen_name'] = self.weibo.screen_name
        except Sina_Token.DoesNotExist, e:
            log.info("info: %s" % e.message)

        try:
            res['taobao_nick'] = self.taobao.screen_name
            res['taobao_token_expires_in'] = self.taobao.expires_in
        except Taobao_Token.DoesNotExist, e:
            log.info("info: %s", e.message)

        try:
            res['wechat_nick'] = self.weixin.nickname
        except WeChat_Token.DoesNotExist, e:
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

    # for set user as authorized author
    # see docs : 授权图文用户

    def get_author_group(self):
        author_group, created =  Group.objects.get_or_create(name="Author")
        return author_group

    def has_author_group(self):
        author_group = self.get_author_group()
        return author_group in self.groups.all()

    # for set user as authorized seller

    def get_seller_group(self):
        seller_group, created = Group.objects.get_or_create(name="Seller")
        return seller_group

    def has_seller_group(self):
        seller_group = self.get_seller_group()
        return seller_group in self.groups.all()


    def refresh_user_permission(self):
        # TODO:  refresh user permission cache here
        pass

    @property
    def is_authorized_author(self):
        return self.has_author_group()

    @property
    def is_authorized_seller(self):
        return self.has_seller_group()

    def setSeller(self, isSeller):
        seller_group = self.get_seller_group()
        if isSeller:
            self.groups.add(seller_group)
        else:
            self.groups.remove(seller_group)
        self.refresh_user_permission()

    def setAuthor(self, isAuthor):
        author_group = self.get_author_group()
        if isAuthor:
            self.groups.add(author_group)
        else:
            self.groups.remove(author_group)
        self.refresh_user_permission()
    @property
    def is_authorized_user(self):
        return self.is_authorized_author or self.is_authorized_seller



    def save(self, *args, **kwargs):
        #TODO  @huanghuang refactor following email related lines into a subroutine
        #
        from apps.core.tasks import send_activation_mail
        from apps.core.tasks.edm import delete_user_from_list
        if self.pk is not None:
            user = GKUser.objects.get(pk=self.pk)
            if user.email != self.email:
                delete_user_from_list(user)
                send_activation_mail(self)
        key = "user:v4:%s" % self.id
        cache.delete(key)
        key = "user:v3:%s" % self.id
        cache.delete(key)
        super(GKUser, self).save(*args, **kwargs)


class Authorized_User_Profile(BaseModel):
    user = models.OneToOneField(GKUser, related_name='authorized_profile')
    # additional column for Authorized Author
    # see  日常开发文档－》授权图文用户
    weixin_id = models.CharField(max_length=255, null=True, blank=True)
    weixin_nick = models.CharField(max_length=255, null=True, blank=True)
    weixin_openid = models.CharField(max_length=255, null=True, blank=True)
    weixin_qrcode_img = models.CharField(max_length=255, null=True, blank=True)
    author_website = models.CharField(max_length=1024, null=True, blank=True)
    weibo_id = models.CharField(max_length=255, null=True, blank=True)
    weibo_nick = models.CharField(max_length=255, null=True, blank=True)
    personal_domain_name = models.CharField(max_length=64, null=True, blank=True)

    rss_url = models.URLField(max_length=255 ,null=True, blank=True)
    points=models.IntegerField(default=0)
    is_recommended_user = models.BooleanField(default=False, db_index=True)


class User_Profile(BaseModel):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, _('man')),
        (Woman, _('woman')),
        (Other, _('other')),
    )

    user = models.OneToOneField(GKUser, related_name='profile')
    nickname = models.CharField(max_length=64, db_index=True)
    location = models.CharField(max_length=32, null=True, default=_('beijing'))
    city = models.CharField(max_length=32, null=True, default=_('chaoyang'))
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              default=Other)
    bio = models.CharField(max_length=1024, null=True, blank=True)
    website = models.CharField(max_length=1024, null=True, blank=True)
    avatar = models.CharField(max_length=255)
    email_verified = models.BooleanField(default=False)


    @property
    def weibo_link(self):
        return "http://weibo.com/u/%s/"%self.weibo_id

    def __unicode__(self):
        return self.nick

    @property
    def nick(self):
        if len(self.nickname) == 32:
            return "guoku_%s" % self.nickname[:8]
        return self.nickname

    @property
    def avatar_url(self):
        if 'http' in self.avatar:
            return self.avatar
        elif self.avatar:
            return "%s%s" % (avatar_host, self.avatar)
        else:
            if self.gender == self.Woman:
                return "%s%s" % (settings.STATIC_URL, 'images/avatar/woman.png')
            return "%s%s" % (settings.STATIC_URL, 'images/avatar/man.png')

    def save(self, *args, **kwargs):
        from apps.core.tasks.edm import update_user_name_from_list
        if self.pk is not None:
            profile = User_Profile.objects.get(pk=self.pk)
            if profile.nickname != self.nickname:
                update_user_name_from_list(self.user)

        key = "user:v4:%s" % self.user.id
        cache.delete(key)
        key = "user:v3:%s" % self.user.id
        cache.delete(key)
        super(User_Profile, self).save(*args, **kwargs)


class User_Follow(models.Model):
    follower = models.ForeignKey(GKUser, related_name="followings")
    followee = models.ForeignKey(GKUser, related_name="fans")
    followed_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")

    def save(self, *args, **kwargs):
        super(User_Follow, self).save(*args, **kwargs)

        key_string = "user_fans_%s" % self.followee.id
        key = md5(key_string.encode('utf-8')).hexdigest()
        cache.delete(key)

        key_string = "user_follow_%s" % self.follower.id
        key = md5(key_string.encode('utf-8')).hexdigest()
        cache.delete(key)


class Banner(BaseModel):
    CONTENT_TYPE_CHOICES = (
        (u'entity', _('entity')),
        (u'category', _('category')),
        (u'user', _('user')),
        (u'user_tag', _('user_tag')),
        (u'outlink', _('outlink')),
    )

    content_type = models.CharField(max_length=64, choices=CONTENT_TYPE_CHOICES)
    key = models.CharField(max_length=1024)
    image = models.CharField(max_length=64, null=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    updated_time = models.DateTimeField(auto_now=True, editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def url(self):
        if 'outlink' == self.content_type:
            return self.key
        elif 'user_tag' == self.content_type:
            type, key = self.key.split(':')
            _url = "guoku://%s/tag/%s/" % (type, key)
            return _url

        _url = "guoku://%s/%s" % (self.content_type, self.key)
        return _url

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)
        # return "%s%s" % ('http://image.guoku.com/', self.image)

    @property
    def has_show_banner(self):
        try:
            self.show
            return True
        except Show_Banner.DoesNotExist:
            return False

    @property
    def position(self):
        try:
            # show = self.show.get(banner = self.id)
            # log.info(self.show.pk)
            return self.show.pk
        except Show_Banner.DoesNotExist:
            return 0


class Show_Banner(BaseModel):
    banner = models.OneToOneField(Banner, related_name='show')
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['id']


# Banner for side bar

class Sidebar_Banner(BaseModel):
    (removed, disabled, enabled) = xrange(3)
    SB_BANNER_STATUS_CHOICE = [
        (removed, _('banner removed')),
        (disabled, _('banner disabled')),
        (enabled, _('banner enabled'))
    ]
    image = models.CharField(max_length=255, null=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    updated_time = models.DateTimeField(auto_now=True, editable=False,
                                        db_index=True)
    link = models.CharField(max_length=255, null=False)
    position = models.IntegerField(null=False, default=1, blank=False)
    status = models.IntegerField(choices=SB_BANNER_STATUS_CHOICE,
                                 default=disabled)

    objects = SidebarBannerManager()

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)

    class Meta:
        ordering = ['-status', 'position', '-updated_time']


class Category(BaseModel):
    title = models.CharField(max_length=128, db_index=True)
    cover = models.CharField(max_length=255)
    status = models.BooleanField(default=True, db_index=True)

    objects = CategoryManager()

    class Meta:
        ordering = ['-status', '-id']

    def __unicode__(self):
        return self.title

    @property
    def sub_category_count(self):
        return self.sub_categories.all().count()

    @property
    def cover_url(self):
        return "%s%s" % (image_host, self.cover)

    @property
    def title_cn(self):
        titles = self.title.split()
        return titles[0]

    @property
    def title_en(self):
        titles = self.title.split()
        if (len(titles) == 2):
            return titles[1]
        return self.title


class Sub_Category(BaseModel):
    group = models.ForeignKey(Category, related_name='sub_categories')
    title = models.CharField(max_length=128, db_index=True)
    alias = models.CharField(max_length=128, db_index=True, default=None)
    icon = models.CharField(max_length=64, null=True, default=None)
    status = models.BooleanField(default=True, db_index=True)

    objects = SubCategoryManager()

    class Meta:
        ordering = ['-status']

    @property
    def icon_large_url(self):
        if self.icon is None:
            return None

        if "images" in self.icon:
            path = self.icon.split("/")
            # log.info("path %s "%path)
            return "http://imgcdn.guoku.com/%s/200/%s" % tuple(path)
        return "http://imgcdn.guoku.com/category/large/%s" % self.icon

    @property
    def icon_small_url(self):
        if self.icon is None:
            return None

        if "images" in self.icon:
            path = self.icon.split("/")
            # log.info("path %s "%path)
            return "http://imgcdn.guoku.com/%s/100/%s" % tuple(path)
        return "http://imgcdn.guoku.com/category/small/%s" % self.icon

    def get_absolute_url(self):
        return "/category/%s/" % self.id

    def v3_toDict(self):
        res = dict()
        # res = self.toDict()
        # res.pop('status', None)
        res['status'] = int(self.status)
        res['group_id'] = self.group_id
        res['category_icon_large'] = self.icon_large_url
        res['category_icon_small'] = self.icon_small_url
        res['category_id'] = self.pk
        if self.title in '+':
            res['category_title'] = self.group.title
        else:
            res['category_title'] = self.title
        return res

    def __unicode__(self):
        return self.title


# TODO: Production Brand
class Brand(BaseModel):
    pending, publish, promotion = xrange(3)
    BRAND_STATUS_CHOICES = [
        (pending, _("pending")),
        (publish, _("publish")),
        (promotion, _("promotion")),
    ]

    name = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100, null=True, default=None)
    icon = models.CharField(max_length=255, null=True, default=None)
    company = models.CharField(max_length=100, null=True, default=None)
    website = models.URLField(max_length=255, null=True, default=None)
    tmall_link = models.URLField(max_length=255, null=True, default=None)
    national = models.CharField(max_length=100, null=True, default=None)
    intro = models.TextField()
    status = models.IntegerField(choices=BRAND_STATUS_CHOICES, default=pending)
    score =  models.IntegerField(default=0, null=False, blank=False)
    created_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-created_date']

    @property
    def icon_url(self):
        if self.icon:
            return "%s%s" % (image_host, self.icon)
        return None

    @property
    def entities(self):
        return SearchQuerySet().models(Entity).filter(brand=self.name)

    # @property
    # def shop_id(self):
    # if len(self.tmall_link) > 0:
    # o = urlparse(self.tmall_link)
    #         qs = parse_qs(o.query)
    #         return qs['shop_id'][0]
    #     return ''

    def __unicode__(self):
        return "%s %s" % (self.name, self.alias)
        # pass


class Entity(BaseModel):
    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = [
        (selection, _("selection")),
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    NO_SELECTION_ENTITY_STATUS_CHOICES = [
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    user = models.ForeignKey(GKUser, related_name='entities', null=True)
    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    category = models.ForeignKey(Sub_Category, related_name='category',
                                 db_index=True)
    brand = models.CharField(max_length=256, default='')
    title = models.CharField(max_length=256, default='')
    intro = models.TextField(default='')
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                                db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    images = ListObjectField()
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    status = models.IntegerField(choices=ENTITY_STATUS_CHOICES, default=new)

    objects = EntityManager()

    class Meta:
        ordering = ['-created_time']

    @property
    def chief_image(self):
        if len(self.images) > 0:
            if 'http' in self.images[0]:
                return self.images[0]
            else:
                return "%s%s" % (image_host, self.images[0])
                # return "%s%s" % ('http://image.guoku.com/', self.images[0])

    @property
    def detail_images(self):
        if len(self.images) > 1:
            return self.images[1:]
            # res = list()
            # for row in self.images[1:]:
            # if image_host in row:
            # res.append(row.replace('imgcdn', 'image'))
            #     else:
            #         res.append(row)
            # return res
        return []

    @property
    def category_name(self):
        return self.category.title + '/' + self.category.group.title

    @property
    def like_count(self):
        key = 'entity:like:%d' % self.pk
        res = cache.get(key)
        if res:
            # log.info("hit hit")
            return res
        else:
            # log.info("miss miss")
            res = self.likes.count()
            cache.set(key, res, timeout=86400)
            return res
            # return self.likes.count()

    @property
    def note_count(self):
        key = 'entity:note:%d' % self.pk
        res = cache.get(key)
        if res:
            # log.info("hit hit")
            return res
        else:
            log.info("miss miss")
            res = self.notes.count()
            cache.set(key, res, timeout=86400)
            return res
            # return self.notes.count()

    @property
    def has_top_note(self):
        if self.notes.filter(status=1):
            return True
        return False

    @property
    def default_buy_link(self):
        buy_link = self.buy_links.filter(default=True).first()
        return buy_link

    def get_top_note_cache_key(self):
        return 'entity:%s:topnote' % self.pk
    @property
    def top_note(self):
        # try:
        cache_key = self.get_top_note_cache_key()
        _tn = cache.get(cache_key,None)
        if _tn is None:
            notes = self.notes.filter(status=1).order_by('-post_time')
            if len(notes) > 0:
                _tn =  notes[0]
                cache.set(cache_key, _tn , 24*3600)
        return _tn


    @property
    def top_note_string(self):
        return self.top_note.note

    def get_absolute_url(self):
        return "/detail/%s/" % self.entity_hash

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    @property
    def mobile_url(self):
        return 'guoku://entity/' + str(self.id) + '/'

    @property
    def selected_related_articles(self):
        related_selection_articles = Selection_Article.objects.published().filter(article__in=self.related_articles.all())
        return  related_selection_articles


    def innr_like(self):
        key = 'entity:like:%d' % self.pk
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, self.likes.count())

    def decr_like(self):
        key = 'entity:like:%d' % self.pk
        if self.likes.count() > 0:
            cache.decr(key)

    def innr_note(self):
        key = 'entity:note:%d' % self.pk
        try:
            cache.incr(key)
        except Exception:
            cache.set(key, int(self.notes.count()))

    @property
    def is_in_selection(self):
        return self.status == Entity.selection

    @property
    def enter_selection_time(self):
        # _tm = None
        try:
            _tm = self.selection_entity.pub_time
        except Exception:
            _tm = self.created_time

        return _tm

    @property
    def selection_hover_word(self):
        return self.brand + ' ' + self.title

    def toDict(self):
        res = super(Entity, self).toDict()
        res['chief_image'] = self.chief_image
        res['detail_images'] = self.detail_images
        res['entity_id'] = self.id
        return res

    def v3_toDict(self, user_like_list=None):
        key = "entity:dict:v3:%s" % self.id
        # key = md5(key_string.encode('utf-8')).hexdigest()
        res = cache.get(key)
        # log.info(user_like_list)
        # res = {}
        if not res:
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
            res['novus_time'] = time.mktime(self.created_time.timetuple())
            res['creator_id'] = self.user_id
            res['old_root_category_id'] = 9
            res['old_category_id'] = 152
            res['total_score'] = 0
            cache.set(key, res, timeout=86400)

        res['note_count'] = self.note_count
        res['like_count'] = self.like_count
        res['like_already'] = 0
        if user_like_list and self.id in user_like_list:
            res['like_already'] = 1

        res['item_list'] = list()
        for b in self.buy_links.all():
            res['item_list'].append(
                b.v3_toDict()
            )
        return res

    def __unicode__(self):
        if len(self.brand) > 0:
            return "%s - %s" % (self.brand, self.title)
        return self.title

    def invalid_top_note_cache(self):
        cache.delete(self.get_top_note_cache_key())

    def save(self, *args, **kwargs):
        super(Entity, self).save(*args, **kwargs)
        key = "entity:dict:v3:%s" % self.id
        # key_string = "entity_v3_%s" % self.id
        # key = md5(key_string.encode('utf-8')).hexdigest()
        cache.delete(key)
        self.invalid_top_note_cache()


    def fetch_image(self):
        image_list = list()
        for image_url in self.images:
            if 'http' not in image_url:
                image_url = 'http:' + image_url
            if image_host in image_url:
                image_list.append(image_url)
                continue

            r = requests.get(image_url, stream=True)
            image = HandleImage(r.raw)
            image_name = image.save()
            image_list.append("%s%s" % (image_host, image_name))
        try:
            self.images = image_list
            self.save()
        except Entity.DoesNotExist, e:
            pass


class Selection_Entity(BaseModel):
    entity = models.OneToOneField(Entity, unique=True)
    is_published = models.BooleanField(default=False)
    pub_time = models.DateTimeField(db_index=True, editable=True)

    objects = SelectionEntityManager()

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.entity.title

    @property
    def publish_timestamp(self):
        return time.mktime(self.pub_time.timetuple())


class Buy_Link(BaseModel):
    (remove, soldout, sale) = xrange(3)
    Buy_Link_STATUS_CHOICES = [
        (sale, _("sale")),
        (soldout, _("soldout")),
        (remove, _("remove")),
    ]
    entity = models.ForeignKey(Entity, related_name='buy_links')
    origin_id = models.CharField(max_length=100, db_index=True)
    origin_source = models.CharField(max_length=255)
    cid = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    foreign_price = models.DecimalField(max_digits=20, decimal_places=2,
                                        default=0)
    volume = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    default = models.BooleanField(default=False)
    shop_link = models.URLField(max_length=255, null=True)
    seller = models.CharField(max_length=255, null=True)
    status = models.PositiveIntegerField(default=sale,
                                         choices=Buy_Link_STATUS_CHOICES)

    class Meta:
        ordering = ['-default']

    def v3_toDict(self):
        res = self.toDict()
        res.pop('link', None)
        res.pop('default', None)
        res['buy_link'] = "http://api.guoku.com%s?type=mobile" % reverse(
            'v4_visit_item', args=[self.origin_id])
        res['price'] = int(self.price)
        return res

    @property
    def amazon_url(self):
        return "%s?tag=guoku-23" % self.link

    def __unicode__(self):
        return self.link


class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity, related_name='likes')
    user = models.ForeignKey(GKUser, related_name='likes')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = EntityLikeManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user')


class Note(BaseModel):
    (remove, normal, top) = (-1, 0, 1)
    NOTE_STATUS_CHOICES = [
        (top, _("top")),
        (normal, _("normal")),
        (remove, _("remove")),
    ]

    user = models.ForeignKey(GKUser, related_name='note')
    entity = models.ForeignKey(Entity, related_name="notes")
    note = models.TextField(null=True, blank=True)
    post_time = models.DateTimeField(auto_now_add=True, editable=False,
                                     db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    status = models.IntegerField(choices=NOTE_STATUS_CHOICES, default=normal)

    objects = NoteManager()

    class Meta:
        ordering = ['-status', 'post_time']
        # unique_together = ('entity', 'user')

    def __unicode__(self):
        return self.note

    @property
    def is_top(self):
        if self.status == self.top:
            return True
        return False

    @property
    def comment_count(self):
        return self.comments.normal().count()

    @property
    def poke_count(self):
        return self.pokes.count()

    @property
    def poke_list(self):
        return self.pokes.all().values_list('user_id', flat=True)

    @property
    def post_timestamp(self):
        return time.mktime(self.post_time.timetuple())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        key = "note:v3:%s" % self.id
        # print key
        cache.delete(key)
        # need update entity topnote cache
        self.entity.invalid_top_note_cache()

        return super(Note, self).save(force_insert=False, force_update=False,
                                      using=None,
                                      update_fields=None)

    def v3_toDict(self, user_note_pokes=None, visitor=None, has_entity=False):
        key = "note:v3:%s" % self.id
        # key = md5(key_string.encode('utf-8')).hexdigest()
        res = cache.get(key)
        # if res:

        if not res:
            res = self.toDict()
            res.pop('note', None)
            res.pop('id', None)
            res.pop('status', None)
            res['note_id'] = self.id
            res['content'] = self.note
            res['created_time'] = time.mktime(self.post_time.timetuple())
            res['updated_time'] = time.mktime(self.updated_time.timetuple())
            res['is_selected'] = self.status
            res['poker_id_list'] = list(self.poke_list)
            cache.set(key, res, timeout=86400)
            log.info("miss miss")
        # log.info(user_note_pokes)
        # log.info(visitor)
        res['poke_count'] = self.poke_count
        res['comment_count'] = self.comment_count
        res['creator'] = self.user.v3_toDict(visitor)
        res['poke_already'] = 0
        if user_note_pokes and self.id in user_note_pokes:
            res['poke_already'] = 1

        if has_entity:
            res['brand'] = self.entity.brand
            res['title'] = self.entity.title
            res['chief_image'] = self.entity.chief_image
            res['category_id'] = self.entity.category_id

        return res


class Note_Comment(BaseModel):
    note = models.ForeignKey(Note, related_name='comments')
    user = models.ForeignKey(GKUser, related_name='note_comment')
    content = models.TextField(null=False)
    replied_comment_id = models.IntegerField(default=None, null=True)
    replied_user_id = models.IntegerField(default=None, null=True)
    post_time = models.DateTimeField(auto_now=True, db_index=True)
    # updated_time = models.DateTimeField(auto_now = True, db_index = True)

    objects = CommentManager()

    class Meta:
        ordering = ['post_time']

    def __unicode__(self):
        return self.content

    def v3_toDict(self):
        res = self.toDict()
        res.pop('user_id', None)
        res.pop('replied_user_id', None)
        res.pop('id', None)
        res['creator'] = self.user.v3_toDict()
        # res['created_time'] = "%s" % self.post_time
        res['created_time'] = time.mktime(self.post_time.timetuple())
        res['comment_id'] = self.id
        try:
            replied_user = GKUser.objects.get(pk=self.replied_user_id)
            res['replied_user'] = replied_user.v3_toDict()
        except GKUser.DoesNotExist:
            pass
        return res


class Note_Poke(models.Model):
    note = models.ForeignKey(Note, related_name="pokes")
    user = models.ForeignKey(GKUser, related_name="poke")
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = NotePokeManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('note', 'user')

        # def save(self, *args, **kwargs):
        #
        #     super(Note_Poke, self).save(*args, **kwargs)
        #     notify.send(self.user, recipient=self.note.user, action_object=self, verb="poke note", target=self.note)

class Sina_Token(BaseModel):
    user = models.OneToOneField(GKUser, related_name='weibo')
    sina_id = models.CharField(max_length=64, null=True, db_index=True)
    screen_name = models.CharField(max_length=64, null=True, db_index=True)
    access_token = models.CharField(max_length=255, null=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.screen_name

    @property
    def weibo_link(self):
        return "http://www.weibo.com/u/%s/" % self.sina_id

    @staticmethod
    def generate(access_token, nick):
        code_string = "%s%s%s" % (
            access_token, nick, time.mktime(datetime.now().timetuple()))
        return md5(code_string.encode('utf-8')).hexdigest()


class Taobao_Token(models.Model):
    user = models.OneToOneField(GKUser, related_name='taobao')
    taobao_id = models.CharField(max_length=64, null=True, db_index=True)
    screen_name = models.CharField(max_length=64, null=True, db_index=True)
    access_token = models.CharField(max_length=255, null=True, db_index=True)
    refresh_token = models.CharField(max_length=255, null=True, db_index=True)
    open_uid = models.CharField(max_length=64, null=True, db_index=True)
    isv_uid = models.CharField(max_length=64, null=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    expires_in = models.PositiveIntegerField(default=0)
    re_expires_in = models.PositiveIntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.screen_name

    @staticmethod
    def generate(user_id, nick):
        code_string = "%s%s%s" % (
            user_id, nick, time.mktime(datetime.now().timetuple()))
        return md5(code_string.encode('utf-8')).hexdigest()


class WeChat_Token(BaseModel):
    user = models.OneToOneField(GKUser, related_name='weixin')
    unionid = models.CharField(max_length=255, db_index=True)
    nickname = models.CharField(max_length=255)
    updated_time = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.nickname

    @staticmethod
    def generate(unionid, nick):
        code_string = "%s%s%s" % (
            unionid, nick, time.mktime(datetime.now().timetuple()))
        return md5(code_string.encode('utf-8')).hexdigest()


from apps.tag.models import Content_Tags
class Article(BaseModel):
    (remove, draft, published) = xrange(3)
    ARTICLE_STATUS_CHOICES = [
        (published, _("published")),
        (draft, _("draft")),
        (remove, _("remove")),
    ]

    creator = models.ForeignKey(GKUser, related_name="articles")
    title = models.CharField(max_length=64)
    identity_code = models.TextField(null=True, blank=True)
    cover = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    publish = models.IntegerField(choices=ARTICLE_STATUS_CHOICES, default=draft)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_datetime = models.DateTimeField()
    showcover = models.BooleanField(default=False)
    read_count = models.IntegerField(default=0)
    feed_read_count = models.IntegerField(default=0)
    # entity cars in in article content
    related_entities = models.ManyToManyField(Entity,
                                              related_name='related_articles')

    objects = ArticleManager()

    class Meta:
        ordering = ["-updated_datetime"]

    def get_dig_key(self):
        return 'article:dig:%d' % self.pk


    @property
    def dig_count(self):
        key = self.get_dig_key()
        res = cache.get(key)
        if res:
            return res
        else:
            res = self.digs.count()
            cache.set(key, res, timeout=3600*24)
            return res

    def incr_dig(self):
        key = self.get_dig_key()
        try:
            cache.incr(key)
        except ValueError:
            cache.set(key, self.digs.count())

    def decr_dig(self):
        key = self.get_dig_key()
        try :
            cache.decr(key)
        except Exception:
            cache.set(key, self.digs.count())

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_updatetime', False):
            self.updated_datetime = datetime.now()
        res = super(Article, self).save(*args, **kwargs)
        # add article related entities,
        hash_list = get_entity_list_from_article_content(self.content)
        entity_list = list(Entity.objects.filter(entity_hash__in=hash_list))
        if entity_list:
            self.related_entities = entity_list
        else:
            self.related_entities = []
        return res

    @property
    def tag_list(self):
        _tag_list = Content_Tags.objects.article_tags(self.id)
        return _tag_list

    @property
    def tags_string(self):
        return ','.join(self.tag_list)

    @property
    def bleached_content(self):
        cover_html = '<img class="article-cover img-responsive" src="%s">' % self.cover_url
        return cover_html + contentBleacher(self.content)

    @property
    def feed_content(self):
        feed_count_img_url = feed_img_counter_host + reverse('article_image_count', args=[self.pk])
        feed_count_img_html = '<div>&nbsp;</div><img src="%s">' % feed_count_img_url
        return  self.bleached_content + feed_count_img_html

    @property
    def digest(self):
        return HTMLParser.HTMLParser().unescape(self.content)

    @property
    def status(self):
        return self.publish

    @property
    def cover_url(self):
        if self.cover:
            if image_host in self.cover:
                return self.cover
            return "%s%s" % (image_host, self.cover)
        return "%s%s" % (
            settings.STATIC_URL, 'images/article/default_cover.jpg')

    @property
    def once_selection(self):
        """

        :return: is the article was in selection at least once.
        """
        # article can be selected multiple times
        res = hasattr(self, 'selections') and (self.selections.count() > 0)
        return res

    @property
    def is_selection(self):
        return self.once_selection

    @property
    def is_draft(self):
        return self.publish == Article.draft

    @property
    def is_published(self):
        return self.publish == Article.published

    @property
    def is_removed(self):
        return self.publish == Article.remove

    @property
    def selection_count(self):
        if not self.once_selection:
            return 0
        else:
            return self.selections.count()

    @property
    def last_selection_time(self):
        if not self.once_selection:
            return _('Never in Selection')

        pubed_selection = self.selections.filter(is_published=True).order_by(
            '-pub_time')
        if pubed_selection:
            return pubed_selection[0].pub_time.strftime('%Y-%m-%d %H:%M')
        else:
            return _('Not Set Selection Pub Time')

    @property
    def related_articles(self):
        return Selection_Article.objects.article_related(self)

    def get_related_articles(self, page=1):
        return Selection_Article.objects.article_related(self, page)

    def get_absolute_url(self):
        return "/articles/%s/" % self.pk

    @property
    def url(self):
        return self.get_absolute_url()

        # will cause circuler reference
        # def tag_string(self):
        #     tids = Content_Tags.objects.filter(target_content_type=31, target_object_id=self.pk).values_list('tag_id', flat=True)
        #     tags = Tags.objects.filter(pk__in=tids)
        #     tag_list=[]
        #     for row in tags:
        #         tag_list.append(row.name)
        #     tag_string = ",".join(tag_list)
        #     return tag_string


# use ForeignKey instead of  oneToOne for selection entity ,
# this means , an article can be published many times , without first been removed from selection
# this design is on propose
# selection_article's is_published is different from article's publish
# editor can only control article's publish
# only article manager can set selection_article's is_published property
class Selection_Article(BaseModel):
    article = models.ForeignKey(Article, unique=False,
                                related_name='selections')
    is_published = models.BooleanField(default=False)
    pub_time = models.DateTimeField(db_index=True, editable=True, null=True,
                                    blank=True)
    create_time = models.DateTimeField(db_index=True, editable=False,
                                       auto_now_add=True, blank=True)

    objects = SelectionArticleManager()

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return '%s- in selection at - %s' % (
            self.article.title, self.create_time)
        # def __unicode__(self):
        #     return self.article


class Article_Dig(BaseModel):
    article = models.ForeignKey(Article, related_name='digs')
    user = models.ForeignKey(GKUser, related_name='digs')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = ArticleDigManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('article', 'user')


class Media(models.Model):
    creator = models.ForeignKey(GKUser, related_name='media_entries')
    file_path = models.URLField()
    content_type = models.CharField(max_length=30)
    upload_datetime = models.DateTimeField(auto_now_add=True, db_index=True,
                                           null=True, editable=False)

    class Meta:
        ordering = ['-upload_datetime']

    @property
    def file_url(self):
        return "%s%s" % (image_host, self.file_path)


# TODO: event banner
class Event(models.Model):
    title = models.CharField(max_length=30, null=False, default='')
    tag = models.CharField(max_length=30, null=False, default='')
    toptag = models.CharField(max_length=30, null=False, default='')
    slug = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    status = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now=True, db_index=True)

    # add related articles
    related_articles = models.ManyToManyField(Article,
                                              related_name='related_events')

    class Meta:
        ordering = ['-created_datetime']

    def __unicode__(self):
        return "%s - %s" % (self.slug, self.title)

    @property
    def has_banner(self):
        count = self.banner.filter(position__gt=0).count()
        if count > 0:
            return True
        return False

    @property
    def banners(self):
        count = self.banner.count()
        return count

    @property
    def has_recommendation(self):
        count = self.recommendation.filter(position__gt=0).count()
        if count > 0:
            return True
        return False

    @property
    def has_articles(self):
        count = self.related_articles.count()
        if count > 0:
            return True
        else:
            return False

    @property
    def recommendations(self):
        count = self.recommendation.count()
        return count

    @property
    def tag_url(self):
        return reverse('tag_entities_url', args=[self.tag.hash])

    @property
    def slug_url(self):
        return reverse('web_event', args=[self.slug])


class Event_Status(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    is_published = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s status : is_published : %s , is_top : %s" % (
            self.event.slug, self.is_published, self.is_top)


# class Event_Articles(BaseModel):
#     event = models.ForeignKey(Event)

class Event_Banner(models.Model):
    (item, shop) = (0, 1)
    BANNER_TYPE__CHOICES = [
        (item, _("item")),
        (shop, _("shop")),
    ]

    image = models.CharField(max_length=255, null=False)
    banner_type = models.IntegerField(choices=BANNER_TYPE__CHOICES,
                                      default=item)
    user_id = models.CharField(max_length=30, null=True)
    link = models.CharField(max_length=255, null=True)
    background_image = models.CharField(max_length=255, null=True, blank=True)
    background_color = models.CharField(max_length=14, null=True, blank=True,
                                        default='fff')
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)
        # return "%s%s" % (image_host, self.image)

    @property
    def background_image_url(self):
        if self.background_image:
            return "%s%s" % (image_host, self.background_image)
        else:
            return None

    @property
    def position(self):
        try:
            return self.show.position
        except Show_Event_Banner.DoesNotExist:
            return 0

    @property
    def has_show_banner(self):
        try:
            self.show
            return True
        except Show_Event_Banner.DoesNotExist:
            return False

    @property
    def event(self):
        try:
            return self.show.event
        except Show_Event_Banner.DoesNotExist, Event.DoesNotExist:
            return None


class Show_Event_Banner(models.Model):
    banner = models.OneToOneField(Event_Banner, related_name='show')
    event = models.ForeignKey(Event, related_name='banner', null=True)
    position = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)

    objects = ShowEventBannerManager()

    class Meta:
        ordering = ['position']


# editor recommendation

class Editor_Recommendation(models.Model):
    image = models.CharField(max_length=255, null=False)
    link = models.CharField(max_length=255, null=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)

    @property
    def section(self):
        try :
            return self.show.section
        except Exception as e :
            # default value , see Show_Editor_Recommendation
            return 'entity'


    @property
    def position(self):
        try:
            return self.show.position
        except Show_Editor_Recommendation.DoesNotExist:
            return 0

    @property
    def has_show_banner(self):
        try:
            self.show
            return True
        except Show_Editor_Recommendation.DoesNotExist:
            return False

    @property
    def event(self):
        try:
            return self.show.event
        except Show_Editor_Recommendation.DoesNotExist, Event.DoesNotExist:
            return None


class Show_Editor_Recommendation(models.Model):

    RECOMMENDATION_SECTION_CHOICE = [
        ('entity','编辑推荐'),
        ('fair','活动一览'),
        ('shop','店铺推荐')]

    recommendation = models.OneToOneField(Editor_Recommendation,
                                          related_name='show', unique=False)
    event = models.ForeignKey(Event, related_name='recommendation', null=True)
    position = models.IntegerField(default=0)
    section = models.CharField(max_length=64,
                               choices=RECOMMENDATION_SECTION_CHOICE,
                               default='entity')
    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)

    class Meta:
        ordering = ['-position']


class Friendly_Link(BaseModel):
    (removed, disabled, enabled) = xrange(3)
    FL_STATUS_CHOICE = [
        (removed, _('banner removed')),
        (disabled, _('banner disabled')),
        (enabled, _('banner enabled'))
    ]

    DesignSite = 'DS'
    Media = 'MEDIA'
    Tech = 'TECH'
    Channel = 'CHANNEL'
    Startup = 'STARTUP'
    Other = 'OTHER'

    LINK_CATEGORY_CHOICE = (
        (DesignSite, _('Design Site')),
        (Media, _('Media Site')),
        (Tech, _('Tech Site')),
        (Channel, _('Channel & Cooperation')),
        (Startup, _('Startup')),
        (Other, _('Other'))
    )
    name = models.CharField(max_length=64, null=False, blank=False)
    link = models.CharField(max_length=255, null=False, blank=False)
    link_category = models.CharField(max_length=64,
                                     choices=LINK_CATEGORY_CHOICE,
                                     default=Other)
    position = models.IntegerField(null=True, default=99)
    logo = models.CharField(max_length=255, null=True, blank=True, default='')
    status = models.IntegerField(choices=FL_STATUS_CHOICE, default=disabled)

    @property
    def logo_url(self):
        return "%s%s" % (image_host, self.logo)


class EDM(BaseModel):
    (
        waiting_for_sd_verify,
        sd_verifying,
        sd_verify_succeed,
        sd_verify_failed,
        send_completed,
    ) = xrange(5)

    EDM_STATUS_CHOICE = [
        (waiting_for_sd_verify, _('waiting for sd verify')),
        (sd_verifying, _('sd verifying')),
        (sd_verify_succeed, _('sd verify succeed')),
        (sd_verify_failed, _('sd verify failed')),
        (send_completed, _('send completed')),
    ]

    title = models.CharField(default=u'本月果库上不可错过的精彩内容，已为你准备好'
                                     u' - 果库 | 精英消费指南',
                             max_length=255)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.IntegerField(choices=EDM_STATUS_CHOICE,
                                 default=waiting_for_sd_verify)
    publish_time = models.DateTimeField(default=datetime.now, null=False)
    cover_image = models.CharField(max_length=255, null=False)
    cover_hype_link = models.CharField(max_length=255, null=False)
    cover_description = models.TextField(null=False)
    sd_template_invoke_name = models.CharField(max_length=255, null=True)
    display = models.BooleanField(default=True)
    selection_articles = models.ManyToManyField(Selection_Article, null=False)
    sd_task_id = models.CharField(max_length=45, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id and not self.pk:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(EDM, self).save(*args, **kwargs)

    @property
    def cover(self):
        cover_image = self.cover_image
        if type(self.cover_image) == list:
            cover_image = self.cover_image[0]

        if 'http' in cover_image:
            return cover_image
        else:
            return "%s%s" % (image_host, cover_image)


class Search_History(BaseModel):
    user = models.ForeignKey(GKUser, null=True)
    key_words = models.CharField(max_length=255, null=False, blank=False)
    ip = models.CharField(max_length=45, null=False, blank=False)
    agent = models.CharField(max_length=255, null=False, blank=False)
    search_time = models.DateTimeField(null=True, blank=False)


class SD_Address_List(BaseModel):
    address = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    created = models.DateTimeField(default=datetime.now())
    members_count = models.IntegerField(default=0)


################################################################################

@receiver(post_save, sender=User_Profile)
def register_signal(sender, instance, created, raw, using,
                        update_fields, **kwargs):
    """ Send a verification email when user registers.
    """
    from apps.core.tasks import send_activation_mail
    if created:
        send_activation_mail(instance.user)


# TODO: model post save
def create_or_update_entity(sender, instance, created, **kwargs):
    if issubclass(sender, Entity):
        log.info(type(instance.status))
        if int(instance.status) == Entity.selection:
            log.info("status %s" % instance.status)
            try:
                selection = Selection_Entity.objects.get(entity=instance)
                selection.entity = instance
                # selection.is_published = False
                # selection.pub_time = datetime.now()
                selection.save()
            except Selection_Entity.DoesNotExist, e:
                log.info(e.message)
                Selection_Entity.objects.create(
                    entity=instance,
                    is_published=False,
                    pub_time=datetime.now()
                )
        else:
            try:
                selection = Selection_Entity.objects.get(entity=instance)
                selection.delete()
            except Selection_Entity.DoesNotExist, e:
                log.info("INFO: entity id %s ,%s" % (instance.pk, e.message))


post_save.connect(create_or_update_entity, sender=Entity,
                  dispatch_uid="create_or_update_entity")


@receiver(post_save, sender=Selection_Entity)
def entity_set_to_selection(sender, instance, created, raw, using,
                            update_fields, **kwargs):
    if created:
        instance.entity.fetch_image()

    if (sender, Selection_Entity) and instance.is_published:
        user = GKUser.objects.get(pk=2)
        notify.send(user, recipient=instance.entity.user,
                    action_object=instance, verb="set selection",
                    target=instance.entity)


def user_like_notification(sender, instance, created, **kwargs):
    if issubclass(sender, Entity_Like) and created:
        # log.info(instance.user)
        # log.info(instance.entity.user)
        if instance.user.is_active == GKUser.remove:
            return
        if instance.user != instance.entity.user and instance.user.is_active >= instance.user.blocked:
            notify.send(instance.user, recipient=instance.entity.user,
                        action_object=instance, verb='like entity',
                        target=instance.entity)


post_save.connect(user_like_notification, sender=Entity_Like,
                  dispatch_uid="user_like_action_notification")


def user_dig_notification(sender, instance, created, **kwargs):
    if issubclass(sender, Article_Dig) and created:
        if instance.user.is_blocked:
            return
        if instance.user !=  instance.article.creator:
            notify.send(instance.user, recipient=instance.article.creator, \
                        action_object=instance, verb='dig article',\
                        target = instance.article)

post_save.connect(user_dig_notification, sender=Article_Dig, \
                  dispatch_uid="user_dig_action_notification")

from apps.tag.tasks import generator_tag
def user_post_note_notification(sender, instance, created, **kwargs):
    data = serializers.serialize('json', [instance])
    generator_tag.delay(data=data)
    # generator_tag(data=data)

    if issubclass(sender, Note) and created:
        # log.info(instance.user)
        instance.entity.innr_note()
        if instance.user != instance.entity.user and instance.user.is_active >= instance.user.blocked:
            notify.send(instance.user, recipient=instance.entity.user,
                        action_object=instance, verb='post note',
                        target=instance.entity)


post_save.connect(user_post_note_notification, sender=Note,
                  dispatch_uid="user_post_note_action_notification")


def user_post_comment_notification(sender, instance, created, **kwargs):
    # log.info(created)
    if issubclass(sender, Note_Comment) and created:
        # log.info(instance.user)
        if instance.user.is_active == GKUser.remove:
            return

        notify.send(instance.user, recipient=instance.note.user,
                    verb="replied note", action_object=instance,
                    target=instance.note)
        if (instance.replied_user_id):
            try:
                user = GKUser.objects.get(pk=instance.replied_user_id)
                notify.send(instance.user, recipient=user,
                            verb="replied comment", action_object=instance,
                            target=instance)
            except GKUser.DoesNotExist, e:
                log.error("Error: %s" % e.message)


post_save.connect(user_post_comment_notification, sender=Note_Comment,
                  dispatch_uid="user_post_comment_action_notification")


def user_poke_note_notification(sender, instance, created, **kwargs):
    if issubclass(sender, Note_Poke) and created:
        if instance.user.is_active == GKUser.remove:
            return
        notify.send(instance.user, recipient=instance.note.user,
                    action_object=instance, verb="poke note",
                    target=instance.note)
        # pass


post_save.connect(user_poke_note_notification, sender=Note_Poke,
                  dispatch_uid="user_poke_note_action_notification")


def user_follow_notification(sender, instance, created, **kwargs):
    if issubclass(sender, User_Follow) and created:
        log.info(instance)
        notify.send(instance.follower, recipient=instance.followee,
                    verb=u'has followed you', action_object=instance,
                    target=instance.followee)


post_save.connect(user_follow_notification, sender=User_Follow,
                  dispatch_uid="user_follow_notification")

#
# def article_related_entity_update(sender, instance, created, **kwargs):
#     if issubclass(sender, Article ):
#         print(instance.content)
#
# post_save.connect(article_related_entity_update, sender=Article, dispatch_uid="article_related_product_update")


__author__ = 'edison7500'
