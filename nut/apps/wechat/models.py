from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# from apps.core.extend.fields.listfield import ListObjectField


# class Robots(models.Model):
#     text, image, voice, video, music, news = range(6)
#     TYPE_CHOICES = (
#         (text, _('text')),
#         (image, _('image')),
#         (voice, _('voice')),
#         (video, _('video')),
#         (music, _('music')),
#         (news, _('news')),
#     )
#
#     # token = models.CharField(max_length=64)
#     accept = models.CharField(_('accept'), max_length=255, unique=True)
#     type = models.IntegerField(choices=TYPE_CHOICES, default=text)
#     content = models.TextField()
#     created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
#
#     class Meta:
#         ordering = ['-created_datetime']

class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='wechat')
    open_id = models.CharField(max_length=255)
    joined_datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return self.open_id


__author__ = 'edison'
