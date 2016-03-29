from apps.core.models import Entity, GKUser, Article
from haystack.forms import SearchForm as haystackSearchForm


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


class APIArticleSearchForm(haystackSearchForm):

    def search(self):
        # sqs = super(APIArticleSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.filter(content=self.cleaned_data['q'], is_selection=True)

        if self.load_all:
            sqs = sqs.load_all()


        # sqs = sqs.filter(is_selection=True)

        return sqs.models(Article).order_by('-read_count')

__author__ = 'edison'
