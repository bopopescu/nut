# coding=utf-8

from django.db  import models
from django.utils.translation import ugettext_lazy as _

from apps.banners.models import BaseBanner


class TopAdBannerQuerySet(models.query.QuerySet):
    pass


class TopAdBannerManager(models.Manager):
    def active_banners(self):
        return self.filter(status__in=[BaseBanner.disabled, BaseBanner.enabled])


class TopAdBanner(BaseBanner):

    DISPLAY_CHOICES = (
        ('app_ios', _('IOS移动端')),
        ('app_android', _('安卓移动端')),
        ('web', _('网站端'))
    )

    CONTENT_TYPE_CHOICES = (
        ('entity', _('entity')),
        ('outlink', _('outlink')),
        ('category', _('category')),
        ('user', _('user')),
    )
    content_type = models.CharField(max_length=64, choices=CONTENT_TYPE_CHOICES, default='entity')
    display_type = models.CharField(max_length=64, choices=DISPLAY_CHOICES, default='app_ios')

    @property
    def url(self):
        if 'outlink' == self.content_type:
            return self.applink
        _url = "guoku://%s/%s" % (self.content_type, self.applink)
        return _url



