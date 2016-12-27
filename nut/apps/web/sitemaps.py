from django.contrib.sitemaps import Sitemap
from apps.core.models import GKUser, Entity, Sub_Category, Article
from apps.tag.models import Tags
from datetime import datetime


class UserSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.6

    def items(self):
        return GKUser.objects.filter(is_active=GKUser.is_active).using('slave')

    def lastmod(self, obj):
        return obj.date_joined

    def location(self, obj):
        return "/u/%s/" % obj.id

class EntitySitemap(Sitemap):
    changefreq = "hourly"
    priority = 1.0
    now = datetime.now()
    def items(self):
        return Entity.objects.filter(updated_time__lte=self.now, status__gte=Entity.freeze).using('slave')

    def lastmod(self, obj):
        return obj.updated_time

    def location(self, obj):
        return  obj.get_absolute_url()

class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    now = datetime.now()

    def items(self):
        return Tags.objects.all().using('slave')

    # def lastmod(self, obj):
    #     return obj.updated_time

    def location(self, obj):
        return obj.get_absolute_url()

class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    # now = datetime.now()
    def items(self):
        return Sub_Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    # template_name = 'web/sitemap/sitemap.xhtml'

    def items(self):
        return Article.objects.filter(publish=Article.published).\
            order_by('-updated_datetime').using('slave')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_datetime

__author__ = 'edison7500'
