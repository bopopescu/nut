from apps.core.forms.search import SearchForm
from apps.core.models import Entity, GKUser


class EntitySearchForm(SearchForm):

    def search(self):
        _keyword = self.get_keyword()
        # print _keyword
        qs = Entity.search.query(_keyword).order_by('@weight', '-created_time')
        return qs


class UserSearchForm(SearchForm):

    def search(self):
        _keyword = self.get_keyword()

        qs = GKUser.search.query(_keyword).order_by('@weight', '-date_joined')
        return qs

__author__ = 'edison'
