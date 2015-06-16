# coding=utf-8
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic import  ListView, View,TemplateView
from django.views.generic.edit import FormView,UpdateView
from django.shortcuts import redirect, get_object_or_404

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

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context = add_side_bar_context_data(context)
        return context

class EditorArticleList(UserPassesTestMixin,ListView):
    def test_func(self, user):
        return  user.is_editor

    template_name = 'web/article/editor_list.html'
    model = Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'articles'
    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user)


class EditorArticleCreate(UserPassesTestMixin, View):
    def test_func(self, user):
        return user.is_editor

    def get(self,request):
        new_article = Article(
            title='这里是文章标题',
            cover='fewfwfew',
            content='这里是文章内容',
            publish=Article.draft,
            creator=self.request.user,
        )
        new_article.save()
        return redirect('web_editor_article_edit',new_article.pk)

class EditorArticleEdit(AjaxResponseMixin,JSONResponseMixin,UserPassesTestMixin,TemplateView):
    fields = ['title']
    template_name = 'web/article/editor_edit.html'
    model = Article

    def get(self, *args, **kwargs):
        pk = kwargs['pk']
        the_article =  get_object_or_404(Article,pk=pk)
        the_form = WebArticleEditForm(instance=the_article)
        return self.render_to_response({
            'form':the_form,
            'pk': pk,
        })

    def post_ajax(self, request, *args, **kwargs):
        res={}
        pk = kwargs.get('pk')
        atform = WebArticleEditForm(request.POST)
        article = get_object_or_404(Article, pk=pk)

        if atform.is_valid():
            try :
                data = atform.data
                article.content = data['content']
                article.title = data['title']
                article.cover = data['cover']
                article.publish = data['publish']
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





    def test_func(self, user):
        return user.is_editor







class DetailView(TemplateResponseMixin, ContextMixin, View):

    template_name =  ""

__author__ = 'edison'
