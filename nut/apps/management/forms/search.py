from apps.core.forms.search import SearchForm
from apps.core.models import Tag, GKUser, Entity

class ManagementSearchForm(SearchForm):

    def search(self):
        _keyword = self.get_keyword()
        _type = self.get_type()
        # _order = self.cleaned_data.get('o', 'time')
        if _type == "t":
            self.res = Tag.search.query(_keyword)
        elif _type == "u":
            self.res = GKUser.search.query(_keyword).order_by('@weight', '-date_joined')
        else:
            self.res = Entity.search.query(_keyword).order_by('@weight', '-created_time')
        return self.res

    def get_type(self):
        self.type = self.cleaned_data.get('t')
        # print len(self.type)
        if len(self.type) == 0:
            return 'e'
        return self.type


__author__ = 'edison'
