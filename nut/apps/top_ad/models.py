# coding=utf-8

from django.db  import models
from django.utils.translation import ugettext_lazy as _

from apps.banners.models import BaseBanner


class TopAdBannerQuerySet(models.query.QuerySet):
    pass


class TopAdBannerManager(models.Manager):
    def ios_top_banners(self):
        return self.active_banners().filter(display_type='app_ios')

    def web_top_banners(self):
        return self.active_banners().filter(display_type='web')

    def android_top_banners(self):
        return self.active_banners().filter(display_type='app_android')

    def active_banners(self):
        return self.filter(status__in=[BaseBanner.enabled])

    def disabled_banners(self):
        return self.filter(status__in=[BaseBanner.disabled])


class TopAdBanner(BaseBanner):

    DISPLAY_CHOICES = (
        ('app_ios', _('IOS')),
        ('app_android', _('Android')),
        ('web', _('WEB'))
    )

    CONTENT_TYPE_CHOICES = (
        ('entity', _('entity')),
        ('outlink', _('outlink')),
        ('category', _('category')),
        ('user', _('user')),
    )

    content_type = models.CharField(max_length=64,
                                    choices=CONTENT_TYPE_CHOICES,
                                    default='entity',
                                    )

    display_type = models.CharField(max_length=64,
                                    choices=DISPLAY_CHOICES,
                                    default='app_ios',
                                    )

    objects = TopAdBannerManager()

    @property
    def url(self):
        if 'outlink' == self.content_type:
            return self.applink
        _url = "guoku://%s/%s" % (self.content_type, self.applink)
        return _url
