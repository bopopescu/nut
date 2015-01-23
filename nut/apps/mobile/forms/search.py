from apps.core.forms.search import SearchForm
from apps.core.models import Entity


class EntitySearchForm(SearchForm):

    def search(self):
        _keyword = self.get_keyword()
        # print _keyword
        qs = Entity.search.query(_keyword).order_by('-created_time')
        return qs

__author__ = 'edison'
