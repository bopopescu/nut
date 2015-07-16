from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from apps.core.models import BaseModel



class Tags(BaseModel):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    hash = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.BooleanField(default=False)
    image = models.URLField(max_length=255)

    def __unicode__(self):
        return self.name

    @property
    def tag_hash(self):
        return self.hash[:8]

    def get_absolute_url(self):
        return "/t/%s/" % self.tag_hash


class Content_Tags(BaseModel):
    tag = models.ForeignKey(Tags)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    target_content_type = models.ForeignKey(ContentType, related_name='tag_target', blank=True, null=True)
    target_object_id = models.BigIntegerField(null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        unique_together = ('tag', 'creator', 'target_content_type', 'target_object_id')

__author__ = 'xiejiaxin'
