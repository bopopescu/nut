#coding=utf-8

import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from apps.notifications.push import JPushSingleMessage, JPushGroupMessage
from apps.core.models import GKUser
# from django.utils.timezone import utc

import jpush
from .signals import notify
from model_utils import managers, Choices


from django.utils.log import getLogger
log = getLogger('django')

from django.conf import settings
app_key = getattr(settings, 'JPUSH_KEY', None)
app_secret = getattr(settings, 'JPUSH_SECRET', None)

now=datetime.datetime.now
if getattr(settings, 'USE_TZ'):
    try:
        from django.utils import timezone
        now = timezone.now
    except ImportError:
        pass


class NotificationQuerySet(models.query.QuerySet):

    def unread(self):
        return self.filter(unread=True)

    def read(self):
        return self.filter(unread=True)

    def mark_all_as_read(self, recipient=None):
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        qs = self.read()
        if recipient:
            qs = qs.filter(recipient=recipient)
        qs.update(unread=True)


class Notification(models.Model):
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default='info', max_length=20)

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor')
    actor_object_id = models.CharField(max_length=255, db_index=True)
    actor = generic.GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType, related_name='notify_action_object', blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = generic.GenericForeignKey('action_object_content_type', 'action_object_object_id')

    timestamp = models.DateTimeField(default=now, db_index=True)

    public = models.BooleanField(default=True)

    objects = managers.PassThroughManager.for_queryset_class(NotificationQuerySet)()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        ctx = {
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.target:
            if self.action_object:
                return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
            return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx

        if self.action_object:
            return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
        return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

    def timesince(self, now=None):
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def marl_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

def notify_handler(verb, **kwargs):

    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    newnotify = Notification(
        recipient = recipient,
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        verb=unicode(verb),
        public=bool(kwargs.pop('public', True)),
        description=kwargs.pop('description', None),
        timestamp=kwargs.pop('timestamp', now())
    )

    for opt in ('target', 'action_object'):
        obj = kwargs.pop(opt, None)
        if not obj is None:
            setattr(newnotify, '%s_object_id' % opt, obj.pk)
            setattr(newnotify, '%s_content_type' % opt, ContentType.objects.get_for_model(obj))

    newnotify.save()

# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')


class DailyPushQuerySet(models.query.QuerySet):
    def pending(self):
        return self.filter(status=DailyPush.pending)

    def sent(self):
        return self.filter(status=DailyPush.sent)

    def disabled(self):
        return self.filter(status=DailyPush.disabled)

class DailyPushManager(models.Manager):
    def get_queryset(self):
        return DailyPushQuerySet(self.model, using=self._db)

    def pending(self):
        return self.get_queryset().pending()

    def sent(self):
        return self.get_queryset().sent()

    def disabled(self):
        return self.get_queryset().disabled()


class DailyPush(models.Model):
    ( pending, sending, sent) = range(3)
    PUSH_STATUS_CHOICES = [
        (pending, _(u"未发送")),
        (sending, _(u"发送中")),
        (sent,_(u"发送完毕"))
    ]

    (user, entity, link) = range(3)
    CONTENT_TYPE_CHOICES = [
        (user, _(u"用户")),
        (entity, _(u"商品")),
        (link,_(u"链接"))
    ]


    push_text = models.CharField(max_length=64)
    push_type = models.IntegerField(choices=CONTENT_TYPE_CHOICES, default=user)
    push_url  = models.CharField(max_length=256)
    send_time = models.DateTimeField(db_index=True)
    status = models.IntegerField(choices=PUSH_STATUS_CHOICES, default=pending, db_index=True)

    object =  DailyPushManager()

    @property
    def message_url(self):
        if self.push_type == self.user :
            return 'guoku://user/%s'%self.push_url
        elif self.push_type == self.entity:
            return 'guoku://entity/%s'%self.push_url
        else:
            return self.push_url

    def __unicode__(self):
        return '%s:%s'%(self.push_text, self.message_url() )

    def send(self):
        pass

    def send_jpush_to_user(self, user):
        rids = user.jpush_rids
        for rid in rids:
            jpush_msg = JPushSingleMessage(rid, self.push_text, self.message_url)
            jpush_msg.send_message()

    def send_to_all(self):
        jpush_msg = JPushGroupMessage(self.push_text, self.message_url)
        jpush_msg.send_message_to_all()



    def send_jpush_by_user_id(self, user_id):
        user = GKUser.objects.get(pk=user_id)
        if user:
            self.send_jpush_to_user(user)




# jpush
class JpushToken(models.Model):
    rid = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='jpush_token', null=True)
    model = models.CharField(max_length=100)
    version = models.CharField(max_length=10)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.rid


from apps.notifications.push import MessageFactroy
def new_push_notification(sender, instance, created, **kwargs):
    MessageFactroy().create_notify_message(sender=sender, instance=instance, created=created, **kwargs)

post_save.connect(new_push_notification, sender=Notification, dispatch_uid='push.notification')

__author__ = 'edison7500'
