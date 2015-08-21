from apps.core.forms.search import SearchForm
from apps.core.models import Entity, GKUser
from haystack.forms import SearchForm as haystackSearchForm

# class EntitySearchForm(SearchForm):
#
#     def search(self):
#         _keyword = self.get_keyword()
#         # print _keyword
#         qs = Entity.search.query(_keyword).order_by('@weight', '-created_time')
#         return qs
#
#
# class UserSearchForm(SearchForm):
#
#     def search(self):
#         _keyword = self.get_keyword()
#
#         qs = GKUser.search.query(_keyword).order_by('@weight', '-date_joined')
#         return qs


class APIEntitySearchForm(haystackSearchForm):

    def search(self):
        sqs = super(APIEntitySearchForm, self).search()
        # print sqs
        if not self.is_valid():
            return self.no_query_found()

        return sqs.models(Entity).order_by('-like_count')


class APIUserSearchForm(haystackSearchForm):

    def search(self):
        sqs = super(APIUserSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        return sqs.models(GKUser).order_by('-fans_count')


__author__ = 'edison'
