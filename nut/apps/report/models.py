from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


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
    (sold_out, category_error, meaningless, malicious) = range(4)

    # TYPE = Choices(_('sold out'), _('category error'), _('meaningless information'), _('malicious information'))
    TYPE = [
        (sold_out, _('sold out')),
        (category_error,  _('category error')),
        (meaningless, _('meaningless information')),
        (malicious, _('malicious information')),
    ]


    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='reporter')
    type = models.CharField(choices=TYPE, default='sold out', max_length=20)
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
    like_total = models.IntegerField(default=0)
    pub_date = models.DateField(db_index=True, editable=False, unique=True)

    class Meta:
        ordering = ['pub_date']

__author__ = 'edison'
