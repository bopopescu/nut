from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger
from django.core.exceptions import ObjectDoesNotExist

# from apps.core.forms.article import
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Article
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.management.decorators import staff_only

from apps.core.mixins.views import SortMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

log = getLogger('django')

from django.views.generic import ListView,View

from apps.core.models import Selection_Article
from apps.core.forms.article import CreateSelectionArticleForm, CreateArticleForms, EditArticleForms, UploadCoverForms


from braces.views import UserPassesTestMixin, JSONResponseMixin


# TODO : add authorise mixin here
class SelectionArticleList(SortMixin,ListView):
    template_name = 'management/article/selection_article_list.html'
    model = Selection_Article
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'selection_article_list'
    default_sort_params = ('create_time','desc')

    def sort_queryset(self, qs, sort_by, order):
        if sort_by:
            qs = qs.order_by(sort_by)
        if order =='desc':
            qs = qs.reverse()
        return qs


class CreateSelectionArticle(UserPassesTestMixin, JSONResponseMixin , View):

    def test_func(self, user):
        return  user.is_chief_editor

    # TODO : use POST for data alter
    def get(self, request, article_id  , *args, **kwargs):
        _form = CreateSelectionArticleForm(data={'article_id':article_id})
        res = {}
        if _form.is_valid():
            _sid = _form.save()
            res['status'] = 'success'
            res['selection_article_id'] = _sid
        else :
            res['status'] = 'fail'
            res['message'] = 'article id not found'

        return self.render_json_response(res)



class RemoveSelectionArticle(UserPassesTestMixin, JSONResponseMixin, View):
    def test_func(self, user):
        return  user.is_chief_editor

    # TODO : use POST for data alter
    def get(self, request, selection_article_id, *args, **kwargs):
        res = {}
        try:
            selection_article = Selection_Article.objects.get(pk=selection_article_id)
        except ObjectDoesNotExist:
            res['status'] = 'fail'
            res['message'] = 'selection article id not found'
            return self.render_json_response(res)

        selection_article.delete()
        res['status'] = 'success'
        res['selection_article_id'] = selection_article_id
        return self.render_json_response(res)


class ArticleList(UserPassesTestMixin,SortMixin,ListView):

    def test_func(self, user):
        return  user.is_chief_editor

    template_name = 'management/article/list.html'
    model = Article
    queryset = Article.objects.filter(publish=Article.published)
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'articles'
    default_sort_params = ('updated_dateime', 'desc')


class DraftArticleList(UserPassesTestMixin, SortMixin, ListView):

    def test_func(self, user):
        return  user.is_chief_editor

    template_name = 'management/article/draft_list.html'
    model = Article
    queryset = Article.objects.filter(publish=Article.draft)
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'articles'
    default_sort_params = ('updated_dateime', 'desc')


# the following function view is deprecated
@login_required
@staff_only
def list(request, template="management/article/list.html"):

    _page = request.GET.get('page', 1)
    article_list = Article.objects.all()
    paginator = ExtentPaginator(article_list, 30)

    try:
        _articles = paginator.page(_page)
    except PageNotAnInteger:
        _articles = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'articles': _articles,
        },
        context_instance = RequestContext(request)
    )


@login_required
@staff_only
def create(request, template="management/article/create.html"):

    if request.method == "POST":
        _forms = CreateArticleForms(user=request.user, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            article = _forms.save()
            # return HttpResponse("OK")
            return HttpResponseRedirect(reverse('management_article_edit', args=[article.pk]))
    else:
        _forms = CreateArticleForms(user=request.user)

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


@csrf_exempt
@login_required
@staff_only
def upload_cover(request, article_id):
    try:
        _article = Article.objects.get(pk = article_id)
    except Article.DoesNotExist, e:
        log.error("Error: %s", e.message)
        raise Http404

    if request.method == "POST":
        _forms =UploadCoverForms(article=_article, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            cover_url = _forms.save()
            return SuccessJsonResponse(data={'cover_url':cover_url})
        log.info(_forms.errors)
    return ErrorJsonResponse(status=400)


@login_required
@staff_only
def edit(request, article_id, template="management/article/edit.html"):

    try:
        _article = Article.objects.get(pk = article_id)
    except Article.DoesNotExist, e:
        log.error("Error: %s", e.message)
        raise Http404

    data = {
        "title": _article.title,
        "content": _article.content,
        "is_publish": _article.publish,
    }

    if request.method == "POST":
        _forms = EditArticleForms(article=_article, data=request.POST, files=request.FILES)
        # log.info(request.POST)
        log.info(_forms)
        if _forms.is_valid():
            _article = _forms.save()

    else:
        _forms = EditArticleForms(_article, data=data)

    return render_to_response(
        template,
        {
            "article": _article,
            "forms": _forms,
        },
        context_instance = RequestContext(request)
    )


@login_required
@staff_only
def preview(request, article_id, template="management/article/preview.html"):

    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404

    return render_to_response(
        template,
        {
            'article':article,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
