from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger

from apps.core.forms.article import CreateArticleForms, EditArticleForms, UploadCoverForms
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Article
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.management.decorators import staff_only

from apps.core.mixins.views import SortMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

log = getLogger('django')

from django.views.generic import ListView
from apps.core.models import Selection_Article

class SelectionArticleList(SortMixin,ListView):
    template_name = 'management/articles/article_list.html'
    model = Selection_Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'selection_article_list'
    default_sort_params = ('pub_time', 'desc')



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
        _forms = EditArticleForms(_article, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()

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
