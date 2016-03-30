from apps.core.views import JSONResponseMixin
from apps.core.utils.http import ErrorJsonResponse
from apps.tag.models import Content_Tags, Tags
from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.v4.models import APISeletion_Articles, APIArticle, APIArticle_Dig
from apps.v4.forms.search import APIArticleSearchForm
from apps.v4.views import APIJsonView
from apps.core.tasks.article import dig_task, undig_task

from haystack.generic_views import SearchView
from django.core.paginator import Paginator
from datetime import datetime
import time


class ArticlesListView(APIJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        sla_list = APISeletion_Articles.objects.\
            published_until(until_time=self.timestamp).\
            order_by('-pub_time')

        paginator = Paginator(sla_list, self.size)

        res = []
        try:
            sla = paginator.page(self.page)
        except Exception:
            return res

        articles_list = list()
        if self.visitor:
            articles_list = APIArticle_Dig.objects.filter(user=self.visitor).values_list('article_id', flat=True)

        for row in sla.object_list:
            a = row.api_article.v4_toDict(articles_list=articles_list)
            a.update(
                {
                    'pub_time': time.mktime(row.pub_time.timetuple()),
                }
            )
            res.append(
                a
            )

        return res

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 10)
        self.timestamp = request.GET.get('timestamp', None)

        _key = request.GET.get('session', None)
        self.visitor = None
        if _key is not None:
            try:
                _session = Session_Key.objects.get(session_key=_key)
                self.visitor = _session.user
            except Session_Key.DoesNotExist:
                pass


        if self.timestamp != None:
            self.timestamp = datetime.fromtimestamp(float(self.timestamp))
        return super(ArticlesListView, self).get(request, *args, **kwargs)


class ArticleView(APIJsonView):

    def get_data(self, context):
        article = APIArticle.objects.get(pk = self.article_id)
        da = list()
        if self.visitor:
            da = APIArticle_Dig.objects.filter(user=self.visitor).values_list('article_id', flat=True)
        return article.v4_toDict(articles_list=da)

    def get(self, request, *args, **kwargs):

        self.article_id = kwargs.pop('article_id', None)
        assert self.article_id is not None

        _key = request.get.GET('session', None)
        self.visitor = None
        try:
            session = Session_Key.objects.get(session_key=_key)
            self.visitor = session.user
        except Session_Key.DoesNotExist, e:
            pass

        return super(ArticleView, self).get(request, *args, **kwargs)

class ArticleSearchView(SearchView, JSONResponseMixin):
    http_method_names = ['get']
    form_class = APIArticleSearchForm

    def get_data(self, context):
        res = {
            'stat' : {
                'all_count' : context.count(),
            },
            'articles' : []
        }
        paginator = Paginator(context, self.size)
        try:
            articles = paginator.page(self.page)
        except Exception:
            return res
        article_ids = map(lambda x: x.article_id, articles.object_list)
        for row in APIArticle.objects.filter(pk__in=article_ids):
            res['articles'].append(
                row.v4_toDict()
            )
        return res

    def form_valid(self, form):
        self.queryset = form.search()
        return self.render_to_json_response(self.queryset)

    def form_invalid(self, form):
        return ErrorJsonResponse(status=400, data=form.errors)

    def get(self, request, *args, **kwargs):
        _key = request.GET.get('session', None)
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 10)
        try:
            _session = Session_Key.objects.get(session_key=_key)
            self.visitor = _session.user
        except Session_Key.DoesNotExist:
            self.visitor = None
        return super(ArticleSearchView, self).get(request, *args, **kwargs)

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleSearchView, self).dispatch(request, *args, **kwargs)


class ArticleTagView(APIJsonView):

    http_method_names = ['get']

    def get_data(self, context):

        res = []

        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            return res
        queryset = Content_Tags.objects.filter(tag=self.tag, target_content_type_id=31)
        articleID_list = queryset.values_list('target_object_id', flat=True)
        article_list = APIArticle.objects.filter(pk__in=articleID_list).order_by('-updated_datetime')

        paginator = Paginator(article_list, self.size)

        try:
            articles = paginator.page(self.page)
        except Exception:
            return res

        for row in articles.object_list:
            res.append(
                row.v4_toDict()
            )

        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 10)
        assert self.tag_name is not None

        return super(ArticleTagView, self).get(request, *args, **kwargs)


class ArticleDigView(APIJsonView):

    http_method_names = ['post']

    def get_data(self, context):
        dig_task.delay(uid=self.session.user_id, aid=self.article_id)
        return {'status': 1, 'article_id': self.article_id}

    def post(self, request, *args, **kwargs):
        _key = request.POST.get('session', None)
        self.article_id = request.POST.get('aid', None)
        assert self.article_id is not None
        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        return super(ArticleDigView, self).post(request, *args, **kwargs)
    # def get(self, request, *args, **kwargs):



class ArticleUnDigView(APIJsonView):
    http_method_names = ['post']

    def get_data(self, context):
        undig_task.delay(uid=self.session.user_id, aid=self.article_id)
        return {'status': 0, 'article_id':self.article_id}

    def post(self, request, *args, **kwargs):
        _key = request.POST.get('session', None)
        self.article_id = request.POST.get('aid', None)
        assert self.article_id is not None
        try:
            self.session = Session_Key.objects.get(session_key=_key)
        except Session_Key.DoesNotExist:
            return ErrorJsonResponse(status=403)
        return super(ArticleUnDigView, self).post(request, *args, **kwargs)
    # def get(self, request, *args, **kwargs):
    #     return super(ArticleUnDigView, self).get(request, *args, **kwargs)


__author__ = 'xiejiaxin'
