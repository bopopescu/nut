import datetime
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.timezone import utc

from model_utils import managers, Choices

now=datetime.datetime.now
if getattr(settings, 'USE_TZ'):
    try:
        from django.utils import timezone
        now = timezone.now
    except ImportError:
        pass


class Notification(models.Model):
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default='info', max_length=20)

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False)

__author__ = 'edison7500'
