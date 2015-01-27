from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from django.db.models import Count
from django.conf import settings

# from apps.core.extend.list_field import ListObjectField
from apps.core.extend.fields.listfield import ListObjectField
from apps.core.manager.account import GKUserManager
from apps.core.manager.entity import EntityManager, EntityLikeManager, SelectionEntityManager
from apps.core.manager.note import NoteManager, NotePokeManager
from apps.core.manager.tag import EntityTagManager
from apps.core.manager.category import CategoryManager, SubCategoryManager
# from apps.core.utils.tag import TagParser

# from apps.notifications import notify

from djangosphinx.models import SphinxSearch
from apps.notifications import notify

import time

log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)

class BaseModel(models.Model):

    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in  self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            d[attr] = "%s" % getattr(self, attr)
        return d


class GKUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    (remove, blocked, active, editor) = (-1, 0, 1, 2)
    USER_STATUS_CHOICES = [
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

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_blocked(self):
        if self.is_active == GKUser.blocked or self.active == GKUser.remove:
            return True
        return False

    @property
    def is_verified(self):
        return self.profile.email_verified

    @property
    def like_count(self):
        return self.likes.count()

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
    def following_list(self):
        return self.followings.all().values_list('followee_id', flat=True)

    @property
    def fans_list(self):
        return self.fans.all().values_list('follower_id', flat=True)

    @property
    def concren(self):
        return  list(set(self.following_list) & set(self.fans_list))

    @property
    def following_count(self):
        return self.followings.count()

    @property
    def fans_count(self):
        return self.fans.count()

    def set_admin(self):
        self.is_admin = True
        self.save()

    def v3_toDict(self, visitor=None):
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
            res['like_count'] = self.like_count
            res['entity_note_count'] = self.post_note_count
            res['tag_count'] = self.tags_count
            res['fan_count'] = self.fans_count
            res['following_count'] = self.following_count
        except Exception, e:
            log.error("Error: user id %s %s", (self.id,e.message))

        if visitor:
            if self.id in visitor.concren:
                res['relation'] = 3
            elif self.id in visitor.following_list:
                res['relation'] = 1
            elif self.id in visitor.fans_list:
                res['relation'] = 2
        return res


    search = SphinxSearch(
        index = 'users',
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )


class User_Profile(BaseModel):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, _('man')),
        (Woman,  _('woman')),
        (Other,  _('other')),
    )

    user = models.OneToOneField(GKUser, related_name='profile')
    nickname = models.CharField(max_length = 64, db_index = True)
    location = models.CharField(max_length = 32, null = True, default = _('beijing'))
    city = models.CharField(max_length = 32, null = True, default = _('chaoyang'))
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = Other)
    bio = models.CharField(max_length = 1024, null = True, blank = True)
    website = models.CharField(max_length = 1024, null = True, blank = True)
    avatar = models.CharField(max_length=255)
    email_verified = models.BooleanField(default = False)

    def __unicode__(self):
        return self.nickname

    @property
    def avatar_url(self):
        if self.avatar:
            return "%s%s" % (image_host, self.avatar)
        else:
            if self.gender == self.Woman:
                return "%s%s" % ('http://www.guoku.com/static/', 'images/woman.jpg')
            return "%s%s" % ('http://www.guoku.com/static/', 'images/man.jpg')
            #     return "%s%s" % (settings.STATIC_URL, 'images/woman.jpg')
            # return "%s%s" % (settings.STATIC_URL, 'images/man.jpg')


class User_Follow(models.Model):
    follower = models.ForeignKey(GKUser, related_name = "followings")
    followee = models.ForeignKey(GKUser, related_name = "fans")
    followed_time = models.DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")

    def save(self, *args, **kwargs):
        super(User_Follow, self).save(*args, **kwargs)
        notify.send(self.follower, recipient=self.followee, verb=u'has followed you', action_object=self, target=self.followee)


class Banner(BaseModel):
    CONTENT_TYPE_CHOICES = (
        (u'entity', _('entity')),
        (u'category', _('category')),
        (u'user', _('user')),
        (u'user_tag', _('user_tag')),
        (u'outlink', _('outlink')),
    )

    content_type = models.CharField(max_length = 64, choices=CONTENT_TYPE_CHOICES)
    key = models.CharField(max_length = 1024)
    image = models.CharField(max_length = 64, null = False)
    created_time = models.DateTimeField(auto_now_add = True, editable=False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, editable=False, db_index = True)

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

    @property
    def has_show_banner(self):
        # if self.show.count() > 0:
        #     return True
        # return False
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
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['id']
    

class Category(BaseModel):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.BooleanField(default = True, db_index = True)

    objects = CategoryManager()
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    @property
    def sub_category_count(self):
        return self.sub_categories.all().count()


class Sub_Category(BaseModel):
    group = models.ForeignKey(Category, related_name='sub_categories')
    title = models.CharField(max_length = 128, db_index = True)
    icon = models.CharField(max_length = 64, db_index = True, null = True, default = None)
    status = models.BooleanField(default = True, db_index = True)

    objects = SubCategoryManager()

    class Meta:
        ordering = ['-id']

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
        return "/c/%s" % self.id

    def v3_toDict(self):
        res = dict()
        # res = self.toDict()
        # res.pop('status', None)
        res['status'] = int(self.status)
        res['group_id'] = self.group_id
        res['category_icon_large'] = self.icon_large_url
        res['category_icon_small'] = self.icon_small_url
        res['category_id'] = self.pk
        res['category_title'] = self.title
        return res

    def __unicode__(self):
        return self.title


class Taobao_Item_Category_Mapping(models.Model):
    taobao_category_id = models.IntegerField(db_index = True, unique = True)
    neo_category_id = models.IntegerField(db_index = True)


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
    category = models.ForeignKey(Sub_Category, related_name='category', db_index=True)
    brand = models.CharField(max_length=256, default='')
    title = models.CharField(max_length=256, default='')
    intro = models.TextField(default='')
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)
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
        # log.info("images, %s" % self.images)
        if len(self.images) > 0:
            if 'http' in self.images[0]:
                return self.images[0]
            else:
                return "%s%s" % (image_host, self.images[0])

    @property
    def detail_images(self):
        if len(self.images) > 1:
            return self.images[1:]
        return []

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def note_count(self):
        return self.notes.count()

    @property
    def has_top_note(self):
        if self.notes.filter(status=1):
            return True
        return False

    @property
    def default_buy_link(self):
        buy_link = self.buy_links.filter(default=True).first()
        return buy_link

    @property
    def top_note(self):
        # try:
        notes = self.notes.filter(status=1)
        if len(notes) > 0:
            return notes[0]
        return None

    def get_absolute_url(self):
        return "/detail/%s" % self.entity_hash

    def toDict(self):
        res = super(Entity, self).toDict()
        res['chief_image'] = self.chief_image
        res['detail_images'] = self.detail_images
        res['entity_id'] = self.id
        res['note_count'] = self.note_count
        res['like_count'] = self.like_count
        return res

    def v3_toDict(self, user_like_list=None):
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
        res['novus_time'] = time.mktime(self.created_time.timetuple())
        res['creator_id'] = self.user_id
        res['old_root_category_id'] = 9
        res['old_category_id'] = 152
        res['total_score'] = 0
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
        return self.title

    search = SphinxSearch(
        index = 'entities',
        weights={
            'brand': 100,
            'title': 50,
            # 'intro': 5,
        },
        maxmatches = 5000,
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )


class Selection_Entity(BaseModel):
    entity = models.OneToOneField(Entity, unique=True)
    is_published = models.BooleanField(default=False)
    pub_time = models.DateTimeField(db_index=True, editable=True)

    objects = SelectionEntityManager()

    class Meta:
        ordering = ['-pub_time']

    def __unicode__(self):
        return self.entity.title

    def save(self, *args, **kwargs):
        super(Selection_Entity, self).save(*args, **kwargs)
        user = GKUser.objects.get(pk=2)
        notify.send(user, recipient=self.entity.user, action_object=self, verb="set selection", target=self.entity)

    @property
    def publish_timestamp(self):
        return time.mktime(self.pub_time.timetuple())

class Buy_Link(BaseModel):
    entity = models.ForeignKey(Entity, related_name='buy_links')
    origin_id = models.CharField(max_length=100)
    origin_source = models.CharField(max_length=255)
    cid = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    volume = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-default']

    def v3_toDict(self):
        res = self.toDict()
        res.pop('link', None)
        res['buy_link'] = "http://api.guoku.com%s?type=mobile" % reverse('mobile_visit_item', args=[self.origin_id])
        res['price'] = int(self.price)
        return res

    def __unicode__(self):
        return self.link


class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity, related_name='likes')
    user = models.ForeignKey(GKUser, related_name='likes')
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)

    objects = EntityLikeManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user')

    def save(self, *args, **kwargs):
        super(Entity_Like, self).save(*args, **kwargs)
        notify.send(self.user, recipient=self.entity.user, action_object=self, verb='like entity', target=self.entity)


class Note(BaseModel):

    (remove, normal, top) = (-1, 0, 1)
    NOTE_STATUS_CHOICES = [
        (top, _("top")),
        (normal, _("normal")),
        (remove, _("remove")),
    ]

    user = models.ForeignKey(GKUser, related_name='note')
    entity = models.ForeignKey(Entity, related_name="notes")
    note = models.TextField(null = True, blank=True)
    post_time = models.DateTimeField(auto_now_add=True, editable=False, db_index = True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    status = models.IntegerField(choices=NOTE_STATUS_CHOICES, default=normal)

    objects = NoteManager()

    class Meta:
        ordering = ['-status','-post_time']
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
        return self.comments.count()

    @property
    def poke_count(self):
        return self.pokes.count()

    @property
    def poke_list(self):
        return self.pokes.all().values_list('user_id', flat=True)


    @property
    def post_timestamp(self):
        return time.mktime(self.post_time.timetuple())

    def save(self, *args, **kwargs):
        super(Note, self).save(*args, **kwargs)
        if self.user != self.entity.user:
            notify.send(self.user, recipient=self.entity.user, action_object=self, verb='post note', target=self.entity)
        # t = TagParser(self.note)
        # t.create_tag(user_id=self.user.pk, entity_id=self.entity_id)

    def v3_toDict(self, user_note_pokes=None, has_entity=False):
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


class Note_Comment(BaseModel):
    note = models.ForeignKey(Note, related_name='comments')
    user = models.ForeignKey(GKUser, related_name='note_comment')
    content = models.TextField(null = False)
    replied_comment_id = models.IntegerField(default=None, null=True)
    replied_user_id = models.IntegerField(default=None, null=True)
    post_time = models.DateTimeField(auto_now = True, db_index = True)
    # updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['post_time']

    def __unicode__(self):
        return self.content

    def save(self, *args, **kwargs):
        super(Note_Comment, self).save(*args, **kwargs)
        notify.send(self.user, recipient=self.note.user, verb="replied", action_object=self, target=self.note)

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
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)

    objects = NotePokeManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('note', 'user')

    def save(self, *args, **kwargs):

        super(Note_Poke, self).save(*args, **kwargs)
        notify.send(self.user, recipient=self.note.user, action_object=self, verb="poke note", target=self.note)


class Tag(models.Model):
    tag = models.CharField(max_length = 128, null = False, unique = True, db_index = True)
    tag_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    status = models.IntegerField(default = 0, db_index = True)
    creator = models.ForeignKey(GKUser, related_name='tags')
    # entity = models.ForeignKey(Entity, related_name='tag')
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('creator', 'tag')

    def __unicode__(self):
        return self.tag

    def get_absolute_url(self):
        return "/t/%s" % self.tag_hash

    search = SphinxSearch(
        index = 'tags',
        mode = 'SPH_MATCH_ALL',
        rankmode = 'SPH_RANK_NONE',
    )


class Entity_Tag(models.Model):
    entity = models.ForeignKey(Entity, related_name='tags')
    user = models.ForeignKey(GKUser, related_name='user_tags')
    tag = models.ForeignKey(Tag, related_name='entities')
    # tag_text = models.CharField(max_length = 128, null = False, db_index = True)
    # tag_hash = models.CharField(max_length = 32, db_index = True)
    # count = models.IntegerField(default = 0)
    created_time = models.DateTimeField(auto_now_add = True, db_index = True)
    last_tagged_time = models.DateTimeField(db_index = True)

    objects = EntityTagManager()

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user', 'tag')


    @property
    def title(self):
        return self.tag.tag

    @property
    def hash(self):
        return self.tag.tag_hash


    # def v3_toDict(self):
    #     res = {}
    #     res['tag_hash'] = self.hash
    #     res['tag'] = self.title
    #
    #
    #     return res
    # def get_absolute_url(self):
    #     return "/t/%s" % self.tag_hash
    #
    # def __unicode__(self):
    #     return self.tag


class Sina_Token(models.Model):
    user = models.OneToOneField(GKUser, related_name='weibo')
    sina_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default=0)
    updated_time = models.DateTimeField(auto_now = True, null = True)

    def __unicode__(self):
        return self.screen_name


class Taobao_Token(models.Model):
    user = models.OneToOneField(GKUser, related_name='taobao')
    taobao_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    refresh_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    re_expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)

    def __unicode__(self):
        return self.screen_name


class Article(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    publish = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True, null=True, editable=False)
    updated_datetime = models.DateTimeField(auto_now=True, db_index=True, null=True, editable=False)


class Media(models.Model):
    file_path = models.URLField()
    content_type = models.CharField(max_length=30)
    upload_datetime = models.DateTimeField(auto_now_add=True, db_index=True, null=True, editable=False)

    class Meta:
        ordering = ['-upload_datetime']

    @property
    def file_url(self):
        return "%s%s" % (image_host, self.file_path)


# event banner
class Event(models.Model):
    title = models.CharField(max_length=30, null=False, default='')
    tag = models.CharField(max_length=30, null=False, default='')
    slug = models.CharField(max_length=100, null=False, db_index=True, unique=True)
    status = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-created_datetime']

    def __unicode__(self):
        return self.slug

    @property
    def has_banner(self):
        count = self.banner.filter(position__gt = 0).count()
        if count > 0:
            return True
        return False

    @property
    def banners(self):
        count = self.banner.count()
        return count

    @property
    def has_recommendation(self):
        count = self.recommendation.filter(position__gt = 0).count()
        if count > 0 :
            return True
        return False

    @property
    def recommendations(self):
        count = self.recommendation.count()
        return count

    @property
    def tag_url(self):
        return reverse('web_tag_detail', args=[self.tag])

    @property
    def slug_url(self):
        return reverse('web_event', args=[self.slug])


class Event_Banner(models.Model):
    (item, shop) = (0, 1)
    BANNER_TYPE__CHOICES = [
        (item, _("item")),
        (shop, _("shop")),
    ]

    image = models.CharField(max_length=255, null=False)
    banner_type = models.IntegerField(choices=BANNER_TYPE__CHOICES, default=item)
    user_id = models.CharField(max_length=30, null=True)
    link = models.CharField(max_length=255, null=True)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)

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
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['position']

# editor recommendation

class Editor_Recommendation(models.Model):
    image = models.CharField(max_length=255, null=False)
    link = models.CharField(max_length=255, null=False)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['-created_time']

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)

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
            return  None


class Show_Editor_Recommendation(models.Model):
    recommendation = models.OneToOneField(Editor_Recommendation, related_name='show', unique=False)
    event = models.ForeignKey(Event, related_name='recommendation', null=True)
    position = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['-position']



__author__ = 'edison7500'