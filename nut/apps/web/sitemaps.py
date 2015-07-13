from django.contrib.sitemaps import Sitemap
from apps.core.models import GKUser, Entity, Tag, Sub_Category, Article
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
        return Tag.objects.filter(created_time__lte=self.now).using('slave')

    def lastmod(self, obj):
        return obj.updated_time

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

    def items(self):
        return Article.objects.filter(publish=Article.published).using('slave')

    def location(self, obj):
        return obj.get_absolute_url()

__author__ = 'edison7500'
