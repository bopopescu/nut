from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from apps.core.models import BaseModel


class Tags(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    hash = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.BooleanField(default=False)
    image = models.URLField(max_length=255)

    def __unicode__(self):
        return self.name


class Content_Tags(BaseModel):
    tag = models.ForeignKey(Tags)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    target_content_type = models.ForeignKey(ContentType, related_name='tag_target', blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)


__author__ = 'xiejiaxin'
