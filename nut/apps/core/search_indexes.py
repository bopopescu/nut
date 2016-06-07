# coding=utf-8

from haystack import indexes
from apps.core.models import Entity, GKUser, Article, Sub_Category
from apps.tag.models import Tags


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    title_auto = indexes.NgramField(model_attr='title')
    def get_model(self):
        return Sub_Category

    def index_queryset(self, using=None):
        return self.get_model().objects.all().using('slave')


class EntityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    entity_id = indexes.IntegerField(model_attr='id')
    entity_hash = indexes.CharField(model_attr='entity_hash')
    title = indexes.CharField(model_attr='title', boost=1.25, faceted=True)
    brand = indexes.CharField(model_attr='brand', boost=1.50, faceted=True)
    user = indexes.CharField(model_attr='user')
    created_time = indexes.DateTimeField(model_attr='created_time')
    price = indexes.FloatField(model_attr='price')
    like_count = indexes.IntegerField(model_attr='like_count')
    # is_in_selection = indexes.BooleanField(model_attr='is_in_selection')

    # category_name = indexes.CharField(model_attr='category_name',boost=1.50, faceted=True)

    # images = indexes.CharField(model_attr='chief_image')

    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Entity

    def prepare_brand(self, obj):
        brand = u''
        if 'brand' in self.prepared_data:
            brand_list = self.prepared_data['brand'].split()
            brand = ''.join(brand_list)
        return brand

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status__gt=Entity.new).using('slave').filter(buy_links__status=2).distinct()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    date_joined = indexes.DateTimeField(model_attr='date_joined')
    is_active = indexes.IntegerField(model_attr='is_active')
    fans_count = indexes.IntegerField(model_attr='fans_count')

    def get_model(self):
        return GKUser

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active__gte=GKUser.active).using('slave')


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.125, faceted=True)
    note_count = indexes.IntegerField(model_attr='note_count')

    tag_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Tags

    def index_queryset(self, using=None):
        return self.get_model().objects.all().using('slave')
#
#
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text            = indexes.CharField(document=True, use_template=True)
    article_id      = indexes.IntegerField(model_attr='id')
    author          = indexes.CharField(model_attr='creator')
    title           = indexes.CharField(model_attr='title', boost=1.125)
    tags            = indexes.CharField(model_attr='tags_string', boost=1.25)
    read_count      = indexes.IntegerField(model_attr='read_count')
    is_selection    = indexes.BooleanField(model_attr='is_selection')

    title_auto      = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publish=Article.published).using('slave')


__author__ = 'edison'
