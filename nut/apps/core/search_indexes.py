from haystack import indexes
from apps.core.models import Entity, GKUser, Article
from apps.tag.models import Tags


class EntityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # id = indexes.IntegerField(model_attr='id')
    title = indexes.CharField(model_attr='title', boost=1.125)
    user = indexes.CharField(model_attr='user')
    created_time = indexes.DateTimeField(model_attr='created_time')
    price = indexes.FloatField(model_attr='price')

    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Entity

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status__gt=Entity.freeze).using('slave')


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GKUser

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active__gte=GKUser.active)


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tags

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
#
#
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='creator')
    title = indexes.CharField(model_attr='title', boost=1.125)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publish=Article.published)


__author__ = 'edison'
