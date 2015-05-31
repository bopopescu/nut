#coding=utf-8

import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import utc

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


# jpush
class JpushToken(models.Model):
    rid = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='jpush_token', null=True)
    model = models.CharField(max_length=100)
    version = models.CharField(max_length=10)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.rid


# def push_notification(verb, **kwargs):
#     kwargs.pop('signal', None)
#
#     _platform = kwargs.pop('platform', 'ios')
#     _register_id = kwargs.pop('rid', None)
#     _production = kwargs.pop('production', True)
#     _instance = kwargs.pop('content_type', None)
#     # print _register_id
#     if _register_id is None:
#         return
#
#     _jpush = jpush.JPush(app_key, app_secret)
#     push = _jpush.create_push()
#     push.audience = jpush.registration_id(_register_id)
#     # push.platform = jpush.audience(_register_id)
#     # log.info(type(verb))
#     ios_msg = jpush.ios(alert=verb.encode('utf8'), badge="+1", extras={'entity':'v1'})
#     push.notification = jpush.notification(alert=verb.encode('utf8'), ios=ios_msg)
#     push.platform = jpush.platform(_platform)
#     # push.audience = jpush.audience({'registration_id':_register_id})
#     push.options = {"time_to_live":86400, "apns_production":_production}
#     push.send()

# push_notify.connect(push_notification, dispatch_uid="notifications.models.jpush")


def push_notification(sender, instance, created, **kwargs):
    if issubclass(instance, Notification):
        log.info(instance)



post_save.connect(push_notification, sender=Notification, dispatch_uid='push.notification')

__author__ = 'edison7500'
