from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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


class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='reporter')
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_datetime']

    def __unicode__(self):
        return self.reporter


class Selection(BaseModel):
    selected_total = models.IntegerField(default=0)
    pub_date = models.DateField(db_index=True, editable=False)

    class Meta:
        ordering = ['pub_date']

__author__ = 'edison'
