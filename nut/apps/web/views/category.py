from datetime import datetime
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic.base import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import ContextMixin
from braces.views import AjaxResponseMixin
from braces.views import JSONResponseMixin
from apps.core.models import Entity, Entity_Like, Article,Selection_Article,Selection_Entity, Sub_Category, Category
from apps.core.extend.paginator import EmptyPage
from apps.core.extend.paginator import PageNotAnInteger
from apps.core.extend.paginator import ExtentPaginator
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.core.utils.http import JSONResponse
from haystack.query import SearchQuerySet


log = getLogger('django')


class CategoryListView(ListView):
    # model = Category
    http_method_names = ['get']
    queryset = Category.objects.filter(status=True)
    template_name = "web/category/all_list.html"
    context_object_name = "categories"


class SubCategoryListView(ListView):
    model = Sub_Category
    template_name = "web/category/list.html"
    context_object_name = "sub_categories"

    def get_queryset(self):
        id = self.kwargs.get('id')
        sub_categories = Sub_Category.objects.filter(group=id).exclude(title='+')
        return sub_categories

    def get_context_data(self, *args, **kwargs):
        id = self.kwargs.get('id')
        context = super(SubCategoryListView, self).get_context_data(*args, **kwargs)
        context['category'] = Category.objects.get(pk=id)
        return context


class CategoryGroupListView(TemplateResponseMixin, ContextMixin, View):
    http_method_names = ['get']
    template_name = 'web/category/detail.html'

    def get_order_by(self):
        order_by = self.kwargs.get('order_by', 'pub_time')
        return order_by

    def get(self, request, *args, **kwargs):
        # log.info(kwargs)

        gid = kwargs.pop('gid', None)
        _page = request.GET.get('page', 1)
        category = Category.objects.get(pk=gid)

        sub_categories_ids = Sub_Category.objects.filter(group=gid).values_list(
            'id', flat=True)

        sub_categories = Sub_Category.objects.filter(group=gid).exclude(title='+')
        if len(sub_categories) > 10:
            sub_categories = sub_categories[:10]

        order_by_like = False
        if self.get_order_by() == 'olike':
            order_by_like = True

        _entity_list = Entity.objects.sort_group(
            category_ids=list(sub_categories_ids),
            like=order_by_like,).filter(buy_links__status=2)

        paginator = ExtentPaginator(_entity_list, 24)
        try:
            _entities = paginator.page(_page)
        except PageNotAnInteger:
            _entities = paginator.page(1)
        except EmptyPage:
            raise Http404
        # log.info(entity_list)

        el = []
        if request.user.is_authenticated():
            e = _entities.object_list
            el = Entity_Like.objects.filter(entity_id__in=tuple(e),
                                            user=request.user).values_list(
                'entity_id', flat=True)

        context = {
            'entities': _entities,
            'user_entity_likes': el,
            'category': category,
            'sub_categories': sub_categories,
            'gid': gid,
            'sort_method': self.get_order_by()
        }
        return self.render_to_response(context)


class OldCategory(RedirectView):
    permanent = True
    pattern_name = 'web_category_detail'

    def get_redirect_url(self, *args, **kwargs):
        try:
            url = reverse(self.pattern_name, args=[self.cid], kwargs=kwargs)
        except NoReverseMatch:
            return None
        return url

    def get(self, request, *args, **kwargs):
        self.cid = kwargs.pop('cid', None)
        assert self.cid is not None
        return super(OldCategory, self).get(request, *args, **kwargs)


class CategoryDetailView(JSONResponseMixin, AjaxResponseMixin, ListView):
    template_name = 'web/category/detail.html'
    model = Entity
    paginate_by = 36
    paginator_class = Jpaginator
    ajax_template_name = 'web/category/cate_selection_ajax.html'

    def get_refresh_time(self):
        refresh_time = self.request.GET \
            .get('t', datetime.now() \
                 .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_category_id(self):
        cid = self.kwargs.get('cid', None)
        return int(cid)

    def get_order_by(self):
        order_by = self.kwargs.get('order_by', 'pub_time')
        return order_by

    def get_queryset(self):
        cid = self.get_category_id()
        order_by_like = False
        if self.get_order_by() == 'olike':
            order_by_like = True
        self.cid = cid
        # e_ids = Selection_Entity.objects.published().filter(entity__category_id=cid).values_list('entity_id', flat=True)
        # entity_list =  Entity.objects.filter(pk__in=e_ids).sort(category_id=cid,like=order_by_like)
        entity_list = Entity.objects.sort(category_id=cid,
                                          like=order_by_like).exclude(
            selection_entity__is_published=False)
        return entity_list

    def get_ajax(self, request, *args, **kwargs):
        status = 1
        self.object_list = getattr(self, 'object_list', self.get_queryset())
        context = self.get_context_data()
        _template = self.ajax_template_name
        _t = loader.get_template(_template)
        _c = RequestContext(
            request,
            context
        )
        try:
            if not context['entities'].has_next():
                status = 0
        except:
            pass
        _data = _t.render(_c)
        return JSONResponse(
            data={
                'data': _data,
                'status': status
            },
            content_type='text/html; charset=utf-8',
        )

    def get_context_data(self, **kwargs):
        order_by = self.get_order_by()
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        entities = context['page_obj']
        el = list()
        sub_category = Sub_Category.objects.get(pk=self.cid)
        category = Category.objects.get(pk=sub_category.group_id)
        # category = sub_category.group
        if self.request.user.is_authenticated():
            if order_by == 'olike':
                e_ids = [r[0] for r in entities.object_list.values_list('id', 'lnumber')]
            else:
                e_ids = list(entities.object_list.values_list('id'))
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=e_ids
                                                    ).using('slave')
        context['cid'] = self.cid
        context['entities'] = entities
        context['sort_method'] = order_by
        context['user_entity_likes'] = el
        context['category'] = category
        context['sub_category'] = sub_category
        context['refresh_datetime'] = self.get_refresh_time()
        context = self.add_related_article(context, sub_category.title)
        return context

    def add_related_article(self, context, category_title):

        article_id_list = SearchQuerySet().models(Article).filter(tags=category_title).values_list('pk', flat=True)
        articles = Article.objects.filter(id__in=article_id_list)
        context['related_articles'] = articles[:3]
        return context