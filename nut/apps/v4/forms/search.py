from apps.core.models import Entity, GKUser, Article
from haystack.forms import SearchForm as haystackSearchForm


class APISearchForm(haystackSearchForm):

    def search(self):
        # self.keyword = self.changed_data['q']
        # print self.keyword
        sqs = super(APISearchForm, self).search()
        # print self.cleaned_data['q']
        res = dict()

        # TODO entities search result
        entity_list = sqs.models(Entity).filter(content=self.cleaned_data['q']).order_by('-created_time')
        entities = list()
        for row in entity_list[:20]:
            entities.append(
                row.object.v3_toDict()
            )
            # print row.object
        # print entities

        # TODO Articles search result
        article_list = sqs.models(Article).filter(content=self.cleaned_data['q'], is_selection=True).order_by('-enter_selection_time')
        articles = list()
        for row in article_list[:10]:
            articles.append(
                row.object.v4_toDict()
            )

        # TODO Users search result
        user_list = sqs.models(GKUser).filter(content=self.cleaned_data['q']).order_by('date_joined')
        users = list()
        for row in user_list[:20]:
            users.append(
                row.object.v3_toDict()
            )

        res.update(
            {
                'entities': entities,
                'articles': articles,
                'users':    users,
            }
        )

        return res


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

        return sqs.models(Article).order_by('-read_count')

__author__ = 'edison'
