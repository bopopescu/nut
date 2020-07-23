# coding=utf-8
from django.utils.translation import gettext as _

from apps.banners.models import BaseBanner
from django.db import models

from apps.core.models import Entity


class SiteBannerQuerySet(models.query.QuerySet):
    def active_banners(self):
        return self.using('subordinate').filter(active_status=True).order_by('position','-updated_time')

    def inactive_banners(self):
        return self.using('subordinate').filter(active_status=False).order_by('position', '-updated_time')


class SiteBannerManager(models.Manager):
    def get_queryset(self):
        return SiteBannerQuerySet(self.model, using=self._db)

    def get_active_banner(self):
        return self.get_queryset().active_banners()

    def get_inactive_banner(self):
        return self.get_queryset().inactive_banners()

    def get_app_banner(self):
        return self.get_active_banner().filter(app_show_status=True)

    def get_mainpage_banner(self):
        return self.get_active_banner().filter(web_mainpage_show_status=True)

    def get_sidebar_banner(self):
        return self.get_active_banner().filter(web_sidebar_show_status=True)


class SiteBanner(BaseBanner):
    STATUS_CHOICE = [
        (False, ('Inactive')),
        (True, ('Active'))
    ]

    SHOW_STATUS_CHOICE = [
        (False, ('disabled')),
        (True, ('enabled'))
    ]
    CONTENT_TYPE_CHOICES = (
        ('entity', ('entity')),
        ('outlink', ('outlink')),
        ('category', ('category')),
        ('user', ('user')),
        ('user_tag', ('user_tag')),
        ('other', ('other')),
    )
    active_status = models.BooleanField(choices=STATUS_CHOICE,default=True)
    content_type = models.CharField(max_length=128, choices=CONTENT_TYPE_CHOICES, default='entity')
    banner_title = models.CharField(max_length=128, null=True, blank=True)
    banner_desc  = models.CharField(max_length=128, null=True, blank=True)
    app_show_status = models.BooleanField(choices=SHOW_STATUS_CHOICE,default=False)
    web_sidebar_show_status = models.BooleanField(choices=SHOW_STATUS_CHOICE, default=False)
    web_mainpage_show_status = models.BooleanField(choices=SHOW_STATUS_CHOICE,default=False)

    objects = SiteBannerManager()

    @property
    def url(self):
        if 'outlink' == self.content_type:
            return self.applink
        elif 'user_tag' == self.content_type:
            type, key = self.applink.split(':')
            _url = "guoku://%s/tag/%s/" % (type, key)
            return _url

        _url = "guoku://%s/%s" % (self.content_type, self.applink)
        return _url

    class Meta:
        db_table = 'sitebanner'


class Entity_Promotion_Manager(models.Manager):
    def index_top_entities(self):
        return self.get_queryset().filter(area='index_top').order_by('pos')

    def index_popular_entities(self):
        return self.get_queryset().filter(area='index_popular').order_by('pos')


class Entity_Promotion(models.Model):
    AREA_CHOICES = (
        ('index_top', _('area_index_top')),
        ('index_popular', _('area_index_popular')),
    )
    entity = models.ForeignKey(Entity, related_name='promotions',null=True, blank=True)
    area = models.CharField(choices=AREA_CHOICES, max_length=32)
    pos = models.IntegerField(default=0)

    objects = Entity_Promotion_Manager()

    class Meta:
        ordering = ['pos']



