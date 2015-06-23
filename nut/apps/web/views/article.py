# coding=utf-8

from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic import  ListView, View,TemplateView, DetailView
from django.views.generic.edit import FormView,UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

from apps.core.models import Article,Selection_Article
from apps.core.mixins.views import SortMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

from apps.web.utils.viewtools import add_side_bar_context_data
from apps.web.forms.articles import WebArticleEditForm


from braces.views import UserPassesTestMixin,JSONResponseMixin,AjaxResponseMixin
from django.utils.log import getLogger
log = getLogger('django')

class ArticleList(ListView):
    def test_func(self, user):
        return  user.is_chief_editor

    template_name = 'web/article/list.html'
    model = Selection_Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'selection_articles'
    # TODO :  make sure the pub time is alright
    default_sort_params = ('pub_time', 'desc')
    #
    # def get_queryset(self):
    #     pass;


    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context = add_side_bar_context_data(context)
        return context

class EditorArticleList(UserPassesTestMixin,ListView):
    def test_func(self, user):
        return  user.can_write;

    template_name = 'web/article/editor_list.html'
    model = Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'articles'
    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user)\
                              .exclude(publish=Article.remove)


class EditorArticleCreate(UserPassesTestMixin, View):
    def test_func(self, user):
        return user.can_write

    def get(self,request):
        new_article = Article(
            title="标题",
            cover='',
            content="正文",
            publish=Article.draft,
            creator=self.request.user,
        )
        new_article.save()
        return redirect('web_editor_article_edit',new_article.pk)

class EditorArticleEdit(AjaxResponseMixin,JSONResponseMixin,UserPassesTestMixin,TemplateView):
    fields = ['title']
    template_name = 'web/article/editor_edit.html'
    model = Article

    def test_func(self, user):
        return user.can_write

    def get(self,request, *args, **kwargs):
        pk = kwargs['pk']
        the_article =  get_object_or_404(Article,pk=pk)

        if request.user.is_writer:
            if the_article.creator != request.user:
                raise Http404('没有找到对应文章，您是作者吗？')



        the_form = WebArticleEditForm(instance=the_article)
        return self.render_to_response({
            'form':the_form,
            'pk': pk,
        })

    def post_ajax(self, request, *args, **kwargs):
        res={}
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        if request.user.is_writer:
            if article.creator != request.user:
                raise Http404('没有找到对应文章，您是作者吗？')

        atform = WebArticleEditForm(request.POST)

        if atform.is_valid():
            try :
                data = atform.cleaned_data
                article.content = data['content']
                article.title = data['title']
                article.cover = data['cover']
                article.publish = data['publish']
                article.showcover = int(data['showcover'])
                article.save()
            except Exception as e:
                log(e)
                res={
                    'error': 1
                }
            res={
                'status':'1',
                'error':0
            }
        else:
            res={
                'status':'0',
                'error':1
            }

        return self.render_to_response(res)

class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'web/article/onepage.html'

    def get_queryset(self):
        return Article.objects.filter(publish=Article.published)

    def get_context_data(self,**kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['is_article_detail'] = True
        context['is_article_creator'] = self.request.user == self.object.creator
        context = add_side_bar_context_data(context)
        return context

class ArticleDelete(UserPassesTestMixin, View):
    def test_func(self, user):
        return user.can_write

    def get(self, request, *args , **kwargs):
        pk = kwargs['pk']
        the_article =  get_object_or_404(Article,pk=pk)

        if request.user.is_writer:
            if the_article.creator != request.user:
                raise Http404('没有找到对应文章，您是作者吗？')

#       TODO : check permission here
        the_article.publish = Article.remove
        the_article.save()
        return redirect('web_editor_article_list')



__author__ = 'edison'
