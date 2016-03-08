
from django.db import  models
from django.conf import  settings
from django.utils.translation import ugettext_lazy as _

from apps.core.models import BaseModel, Media


image_host = getattr(settings, 'IMAGE_HOST', None)


class BaseBanner(BaseModel):
    (removed, disabled, enabled) = xrange(3)
    BANNER_STATUS_CHOICE = [
        (removed, _('banner removed')),
        (disabled, _('banner disabled')),
        (enabled, _('banner enabled'))
    ]

    image = models.CharField(max_length=255, null=False)

    created_time = models.DateTimeField(auto_now_add=True, editable=False,
                                        db_index=True)
    updated_time = models.DateTimeField(auto_now=True, editable=False,
                                        db_index=True)
    link = models.CharField(max_length=255, null=False)
    applink = models.CharField(max_length=255, null=False)
    position = models.IntegerField(null=False, default=1, blank=False)
    status = models.IntegerField(choices=BANNER_STATUS_CHOICE,default=disabled)

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)

    class Meta:
        abstract = True
        ordering = ['-status', 'position', '-updated_time']










