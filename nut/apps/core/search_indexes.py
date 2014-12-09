from haystack import indexes
from apps.core.models import Entity


class EntityIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(document=True, use_template=True)
    


    def get_model(self):
        return Entity

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

__author__ = 'edison'
