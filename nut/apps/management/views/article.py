from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.log import getLogger

from apps.core.forms.article import CreateArticleForms, EditArticleForms
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Article

log = getLogger('django')


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

def create(request, template="management/article/create.html"):

    if request.method == "POST":
        _forms = CreateArticleForms(request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()
            return HttpResponse("OK")
    else:
        _forms = CreateArticleForms()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


def edit(request, article_id, template="management/article/edit.html"):

    try:
        article = Article.objects.get(pk = article_id)
    except Article.DoesNotExist, e:
        log.error("Error: %s", e.message)
        raise Http404

    data = {
        "title": article.title,
        "content": article.content,
        "is_publish": article.publish,
    }

    if request.method == "POST":
        _forms = EditArticleForms(article, request.POST, request.FILES)
        if _forms.is_valid():
            _forms.save()

    else:
        _forms = EditArticleForms(article, data=data)

    return render_to_response(
        template,
        {
            "forms": _forms,
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
