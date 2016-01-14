from django.db import models
from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from django.db.models.signals import post_save
import requests


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

    (pending, in_hand, processed) = xrange(3)

    PROGRESS = [
        (processed, _('processed')),
        (in_hand, ('in hand')),
        (pending, _('process pending')),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='reporter')
    type = models.PositiveSmallIntegerField(choices=TYPE, default=sold_out)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    progress = models.PositiveSmallIntegerField(choices=PROGRESS, default=pending)
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


def process_report(sender, instance, created, **kwargs):
    # print sender
    if issubclass(sender, Report) and created:
        if instance.content_type.model == 'entity':
            for row in instance.content_object.buy_links.filter(origin_source='taobao.com'):
                # print row
                if row.status == 0:
                    continue
                data = {
                    'project':'default',
                    'spider':'taobao',
                    'setting':'DOWNLOAD_DELAY=2',
                    'item_id': row.origin_id,
                }
                # print data
                res = requests.post('http://10.0.2.49:6800/schedule.json', data=data)
            # instance.process = Report.progress
            # instance.save()


post_save.connect(process_report, sender=Report, dispatch_uid='process.report')

__author__ = 'edison'
