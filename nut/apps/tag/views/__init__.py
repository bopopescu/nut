from django.views.generic import ListView
from django.http import Http404
from apps.tag.models import Tags, Content_Tags
from apps.core.extend.paginator import ExtentPaginator
from apps.core.models import Entity_Like, Note
from django.utils.log import getLogger
from django.shortcuts import get_object_or_404
from django.db.models import Count
from braces.views import JSONResponseMixin, AjaxResponseMixin
import urllib


log = getLogger('django')


class TagListView(ListView):
    queryset = Tags.objects.all()
    http_method_names = ['get']
    template_name = 'tag/list.html'


class TagEntitiesByHashView(AjaxResponseMixin, JSONResponseMixin, ListView):
    paginate_by = 20
    paginator_class = ExtentPaginator
    template_name = 'tag/entities.html'
    ajax_template_name = 'tag/partial/ajax_entities.html'
    context_object_name = 'entities'

    def get_queryset(self):
        self.tag_hash = self.kwargs.pop('tag_hash', None)
        self.tag = _tag = get_object_or_404(Tags, hash=self.tag_hash)
        if _tag:
            return Content_Tags.objects.filter(tag=_tag,
                                               target_content_type_id=24) \
                .annotate(tCount=Count('tag'))
        else:
            return None

    def get_refresh_time(self):
        refresh_time = self.request.GET \
            .get('t', datetime.now() \
                 .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = getattr(self, 'object_list', self.get_queryset())
        context = self.get_context_data()
        _template = self.ajax_template_name
        _t = loader.get_template(_template)
        _c = RequestContext(request, context)
        _html = _t.render(_c)

        return self.render_json_response({
            'data': _html,
            'status': 1,
            'errors': 0,
        })

    def get_context_data(self, **kwargs):
        context = super(TagEntitiesByHashView, self).get_context_data(**kwargs)
        entities = context['page_obj']
        context['refresh_time'] = self.get_refresh_time()
        content_tag_list = context['object_list']
        el = []
        if self.request.user.is_authenticated():
            note_id_list = content_tag_list.values_list("target_object_id",
                                                        flat=True)
            eid_list = Note.objects.filter(pk__in=list(note_id_list)) \
                .values_list('entity_id', flat=True)
            el = Entity_Like.objects.filter(entity_id__in=list(eid_list),
                                            user=self.request.user) \
                .values_list('entity_id', flat=True)

        context.update({
            'tag': self.tag,
            'user_entity_likes': el,
            'entities': entities
        })
        return context


class TagEntityView(ListView):
    http_method_names = ['get']
    template_name = 'tag/entities.html'
    paginate_by = 20
    paginator_class = ExtentPaginator

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag,
                                                    target_content_type_id=24)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagEntityView, self).get_context_data(**kwargs)
        contenttag_list = res['object_list']
        el = []
        if self.request.user.is_authenticated():
            note_id_list = contenttag_list.values_list("target_object_id",
                                                       flat=True)
            eid_list = Note.objects.filter(
                pk__in=list(note_id_list)).values_list('entity_id', flat=True)
            el = Entity_Like.objects.filter(entity_id__in=list(eid_list),
                                            user=self.request.user).values_list(
                'entity_id', flat=True)

        res.update(
            {
                'tag': self.tag,
                'user_entity_likes': el,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        assert self.tag_name is not None

        self.tag_name = self.tag_name.lower()
        return super(TagEntityView, self).get(request, *args, **kwargs)
        # return self.render_to_response(context={})


class TagArticleView(ListView):
    http_method_names = ['get']
    template_name = 'tag/articles.html'
    paginate_by = 20
    paginator_class = ExtentPaginator

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag,
                                                    target_content_type_id=31)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagArticleView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        self.tag_name = urllib.unquote(str(self.tag_name)).decode('utf-8')

        assert self.tag_name is not None

        return super(TagArticleView, self).get(request, *args, **kwargs)


from django.template import loader, RequestContext
from apps.core.models import Article
from datetime import datetime
from apps.counter.utils.data import RedisCounterMachine


class NewTagArticleView(JSONResponseMixin, AjaxResponseMixin, ListView):
    template_name = 'tag/tag_articles.html'
    ajax_template_name = 'tag/partial/ajax_article_item_list_new.html'
    paginate_by = 12
    paginator_class = ExtentPaginator
    context_object_name = 'articles'

    def get_tag_name(self):
        tag_name = self.kwargs.pop('tag_name', None)
        return urllib.unquote(str(tag_name)).decode('utf-8')

    def get_refresh_time(self):
        refresh_time = self.request.GET \
            .get('t', datetime.now() \
                 .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_queryset(self):
        tag_name = self.get_tag_name()
        self.tag = get_object_or_404(Tags, name=tag_name)
        article_ids = Content_Tags.objects.filter(tag=self.tag,
                                                  target_content_type_id=31).values_list(
            'target_object_id', flat=True)
        return Article.objects.filter(pk__in=article_ids,
                                      selections__is_published=True,
                                      selections__pub_time__lte=datetime.now())

    def get_ajax(self, request, *args, **kwargs):
        # TODO : add error handling here
        self.object_list = getattr(self, 'object_list', self.get_queryset())
        context = self.get_context_data()
        _template = self.ajax_template_name
        _t = loader.get_template(_template)
        _c = RequestContext(request, context)
        _html = _t.render(_c)

        return self.render_json_response({
            'html': _html,
            'errors': 0,
            'has_next_page': context['has_next_page']
        }, status=200)

    def get_read_counts(self, articles):
        counts_dic = RedisCounterMachine.get_read_counts(articles)
        return counts_dic

    def get_context_data(self, **kwargs):
        context = super(NewTagArticleView, self).get_context_data(**kwargs)
        context['refresh_time'] = self.get_refresh_time()
        context['has_next_page'] = context['page_obj'].has_next()
        context['top_article_tags'] = Tags.objects.top_article_tags()
        context['tag'] = self.tag
        context['top_article_tags'] = Tags.objects.top_article_tags()

        articles = context['articles']

        try:
            # make sure use try catch ,
            # if statistic is down
            # the view is still working
            context['read_count'] = self.get_read_counts(articles)

        except Exception as e:
            log.info('the fail to load read count')
            log.info(e.message)

        return context


__author__ = 'xiejiaxin'
