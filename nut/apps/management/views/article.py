from django.forms import HiddenInput
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse , reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.log import getLogger
from django.utils.translation import gettext_lazy as _

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Article, GKUser
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.management.decorators import staff_only

from apps.core.mixins.views import SortMixin, FilterMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

log = getLogger('django')

from django.views.generic import ListView, View
from apps.core.views import BaseFormView

from apps.core.models import Selection_Article
from apps.core.forms.article import CreateSelectionArticleForm, \
    EditSelectionArticleForm, \
    CreateArticleForms, \
    EditArticleForms, \
    UploadCoverForms

from apps.tag.models import Content_Tags, Tags
from braces.views import UserPassesTestMixin, JSONResponseMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.api.serializers.articles import ArticleSerializer

from django.views.generic.edit import UpdateView


class RESTfulArticleListView(APIView):
    def get(self,request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RESTfulArticleDetail(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk , format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def post(self,request, pk , format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from apps.management.forms.article import UpdateArticleForm
class UpdateArticleView(UpdateView):
    model = Article
    template_name = 'management/article/new_edit.html'
    form_class = UpdateArticleForm
    def get_initial(self):
        initial = super(UpdateArticleView, self).get_initial()
        _article = self.get_object()
        tids = Content_Tags.objects.filter(target_content_type=31, target_object_id=_article.id).values_list('tag_id', flat=True)
        tags = Tags.objects.filter(pk__in=tids)
        tag_list = []
        for row in tags:
            tag_list.append(row.name)
        tag_string = ",".join(tag_list)
        initial['tags'] = tag_string
        initial['creator'] = _article.creator
        return initial

    # success_url = reverse('management_article_list')




# TODO : add authorise mixin here
class SelectionArticleList(UserPassesTestMixin,FilterMixin, SortMixin,ListView):
    template_name = 'management/article/selection_article_list.html'
    model = Selection_Article
    queryset = Selection_Article.objects.filter(is_published=True)
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'selection_article_list'
    default_sort_params = ('pub_time','desc')

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(article__title__icontains=filter_value)
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by:
            qs = qs.order_by(sort_by)
        if order =='desc':
            qs = qs.reverse()
        return qs

    def test_func(self, user):
        return user.is_chief_editor


class SelectionPendingArticleList(UserPassesTestMixin, SortMixin,ListView):
    template_name = 'management/article/selection_article_list.html'
    model = Selection_Article
    queryset = Selection_Article.objects.filter(is_published=False)
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

    def test_func(self, user):
        return user.is_chief_editor


class CreateSelectionArticle(UserPassesTestMixin, JSONResponseMixin , View):

    def test_func(self, user):
        return  user.is_chief_editor

    # TODO : use POST for data alter
    def get(self, request, article_id, *args, **kwargs):
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


class EditSelectionArticle(UserPassesTestMixin, BaseFormView):

    template_name = 'management/article/edit_selection.html'
    form_class = EditSelectionArticleForm

    def test_func(self, user):
        return user.is_chief_editor

    def get_form_class(self, **kwargs):
        sla = kwargs.pop('sla')
        k = self.get_form_kwargs()
        k.update(
            {
                'sla':sla
            }
        )
        return self.form_class(**k)

    def get(self, request, sla_id, *args, **kwargs):
        # _form = EditSelectionArticleForm
        try:
            sla = Selection_Article.objects.get(pk = sla_id)
        except Selection_Article.DoesNotExist:
            raise Http404

        self.initial = {
            'article_id': sla.article.id,
            'is_published': int(sla.is_published),
            'pub_time': sla.pub_time,
        }
        context = {
            'form':self.get_form_class(sla=sla),
            'sla': sla,
            'button': _('save'),
        }
        return self.render_to_response(context=context)

    def post(self, request, sla_id, *args, **kwargs):
        try:
            sla = Selection_Article.objects.get(pk = sla_id)
        except Selection_Article.DoesNotExist:
            raise Http404

        # self.initial = {
        #     'article_id': sla.article.id,
        #     'is_published': int(sla.is_published),
        #     'pub_time': sla.pub_time,
        # }

        form = self.get_form_class(sla=sla)
        if form.is_valid():
            form.save()
        context = {
            'form':self.get_form_class(sla=sla),
            'sla': sla,
            'button': _('save'),
        }
        return self.render_to_response(context=context)
        # return self.


class RemoveSelectionArticle(UserPassesTestMixin, JSONResponseMixin, View):
    def test_func(self, user):
        return  user.is_chief_editor

    # TODO : use POST for data alter
    def get(self, request, selection_article_id, *args, **kwargs):
        res = {}
        try:
            selection_article = Selection_Article.objects.get(pk=selection_article_id)
        except Selection_Article.DoesNotExist:
            res['status'] = 'fail'
            res['message'] = 'selection article id not found'
            return self.render_json_response(res)

        selection_article.delete()
        res['status'] = 'success'
        res['selection_article_id'] = selection_article_id
        return self.render_json_response(res)

# TODO : use a parent class for 3 article list  view


class BaseManagementArticleListView(UserPassesTestMixin, SortMixin, ListView):
    template_name = 'management/article/list.html'
    model = Article
    paginate_by = 30
    paginator_class = Jpaginator
    context_object_name = 'articles'
    default_sort_params = ('updated_datetime', 'desc')

    def test_func(self, user):
        return user.is_editor or user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(BaseManagementArticleListView, self).get_context_data(*args, **kwargs)
        context['authorized_authors'] = GKUser.objects.authorized_author()
        return context


class AuthorArticlePersonList(BaseManagementArticleListView):
    def get_queryset(self):
        _user_id = self.kwargs.pop('pk', None)
        if _user_id is None :
            raise  Http404
        else:
            return Article.objects.filter(publish=Article.published,creator__id=_user_id)\
                    .order_by('-updated_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorArticlePersonList, self).get_context_data(*args, **kwargs)
        context['for_author'] = True
        return context

class AuthorArticleList(BaseManagementArticleListView):
    def get_queryset(self):

        authorized_authors = GKUser.objects.authorized_author()
        return  Article.objects.filter(publish=Article.published, creator__in=authorized_authors)\
                        .order_by('-updated_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorArticleList, self).get_context_data(*args, **kwargs)
        context['for_author'] = True
        return context


class ArticleList(BaseManagementArticleListView):
    def get_queryset(self):
        authorized_authors = GKUser.objects.authorized_author()
        return Article.objects.filter(publish=Article.published).exclude(creator__in=authorized_authors)


class DraftArticleList(UserPassesTestMixin, SortMixin, ListView):

    def test_func(self, user):
        return user.is_editor

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

    # tids = Content_Tags.objects.filter(target_content_type=31, target_object_id=_article.id).values_list('tag_id', flat=True)
    # # print tids
    # tags = Tags.objects.filter(pk__in=tids)
    # tag_list = []
    # for row in tags:
    #     tag_list.append(row.name)

    tag_string = _article.tags_string

    data = {
        "title": _article.title,
        "content": _article.content,
        "is_publish": _article.publish,
        "author": _article.creator_id,
        "tags": tag_string,
    }

    if request.method == "POST":
        _forms = EditArticleForms(article=_article, data=request.POST, files=request.FILES)
        # log.info(request.POST)
        # log.info(_forms)
        if _forms.is_valid():
            _article = _forms.save()
            return HttpResponseRedirect(request.GET.get('prev', request.path))


    else:
        _forms = EditArticleForms(_article, data=data)

    return render_to_response(
        template,
        {
            "article": _article,
            "forms": _forms,
            "tag_url": reverse_lazy('web_article_textrank', _article.pk)
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


