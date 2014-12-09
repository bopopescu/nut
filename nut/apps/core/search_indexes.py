from haystack import indexes
from apps.core.models import Entity


class EntityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    user = indexes.CharField(model_attr='user')
    created_time = indexes.DateTimeField(model_attr='created_time')


    def get_model(self):
        return Entity

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

__author__ = 'edison'
