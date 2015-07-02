# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import  ListView,\
                                  View,\
                                  TemplateView,\
                                  DetailView
from django.shortcuts import redirect, get_object_or_404,render
from django.http import Http404
from django.template import RequestContext, loader

from apps.core.models import Article,Selection_Article
from apps.core.mixins.views import SortMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator

from apps.web.utils.viewtools import add_side_bar_context_data
from apps.web.forms.articles import WebArticleEditForm
from apps.counter.utils.data import RedisCounterMachine

from braces.views import UserPassesTestMixin,JSONResponseMixin,AjaxResponseMixin
from django.utils.log import getLogger

from datetime import datetime
log = getLogger('django')


class SelectionArticleList(AjaxResponseMixin,ListView):
    template_name = 'web/article/selection_list.html'
    model = Selection_Article
    paginate_by = 15
    paginator_class = Jpaginator
    context_object_name = 'selection_articles'
    #
    # def get_queryset(self):
    #     pass;
    
    def get_refresh_time(self):
        refresh_time = self.request.GET\
                                    .get('t',datetime.now()\
                                                     .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_queryset(self):
        qs = Selection_Article.objects\
                              .published_until(self.get_refresh_time())\
                              .order_by('-pub_time')
        return qs

    def get_ajax(self, request, *args, **kwargs):
        context = self.get_context_data()
        _template = 'web/article/selection_ajax_list.html'
        return render(request, _template, context)

    def get_read_counts(self,articles):
        counts_dic = RedisCounterMachine.get_read_counts(articles)
        return counts_dic

    def get_context_data(self, **kwargs):
        context = super(SelectionArticleList, self).get_context_data(**kwargs)
        selection_articles = context['selection_articles']
        articles = [sla.article for sla in selection_articles]
        try :
            # make sure use try catch ,
            # if statistic is down
            # the view is still working
            context['read_count'] = self.get_read_counts(articles)
        except Exception as e :
            log.info('the fail to load read count')
            log.info(e.message)

        context = add_side_bar_context_data(context)
        return context


class EditorDraftList(UserPassesTestMixin,ListView):
    def test_func(self, user):
        return  user.can_write;

    template_name = 'web/article/editor_list.html'
    model = Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'articles'
    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user,publish=Article.draft)


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

        return self.render_json_response(res)

class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'web/article/onepage.html'

    def get_queryset(self):
        return Article.objects.filter(publish=Article.published)

    def get_context_data(self,**kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        article = context['article']
        context['is_article_detail'] = True
        context['is_article_creator'] = self.request.user == self.object.creator
        context['can_show_edit'] =  (not article.is_selection) and (self.request.user == article.creator)
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
