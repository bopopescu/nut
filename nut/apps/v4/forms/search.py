#encoding=utf-8
from haystack.forms import SearchForm as haystackSearchForm
from apps.core.models import Entity, GKUser, Article
from apps.v4.schema.articles import ArticleSchema

from django.utils.log import getLogger
import re

log = getLogger('django')

article_schema   = ArticleSchema()

regex  = re.compile('-|－')

class APISearchForm(haystackSearchForm):

    def clean_q(self):
        q           = self.cleaned_data.get('q', None)
        keyword     = regex.sub(' ', q)
        log.info("keyword %s", keyword)
        return keyword

    def search(self):
        sqs = super(APISearchForm, self).search()
        res = dict()

        # TODO entities search result
        entity_list = sqs.models(Entity).filter(content=self.cleaned_data['q']).order_by('-read_count')
        entities = list()
        for row in entity_list[:10]:
            try:
                entities.append(
                    row.object.v3_toDict()
                )
            except Exception as e:
                log.info(e.message)

        # TODO Articles search result
        article_list = sqs.models(Article).filter(content=self.cleaned_data['q'], is_selection=True).order_by('-like_count')
        articles = list()
        for row in article_list[:10]:
            try:
                articles.append(
                    article_schema.dump(row.object, many=False).data
                )
            except Exception as e:
                log.error(e.message)

        # TODO Users search result
        user_list = sqs.models(GKUser).filter(content=self.cleaned_data['q']).order_by('-fans_count')
        users = list()
        for row in user_list[:20]:
            try:
                users.append(
                    row.object.v3_toDict()
                )
            except Exception as e:
                log.info(e.message)

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
