from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='reporter')
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return self.reporter

__author__ = 'edison'
