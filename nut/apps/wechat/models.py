from django.db import models
from django.utils.translation import ugettext_lazy as _


class Robots(models.Model):
    text, image, voice, video, music, news = range(6)
    TYPE_CHOICES = (
        (text, _('text')),
        (image, _('image')),
        (voice, _('voice')),
        (video, _('video')),
        (music, _('music')),
        (news, _('news')),
    )

    token = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPE_CHOICES, default=text)
    content = models.TextField()




__author__ = 'edison'
