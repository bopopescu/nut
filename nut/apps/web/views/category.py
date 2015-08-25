from datetime import  datetime

from django.shortcuts import render_to_response
from django.http import Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext
from django.views.generic import ListView, RedirectView
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

from apps.core.models import Category, Sub_Category, Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
# from django.db.models import Count

from django.utils.log import getLogger
log = getLogger('django')


class CategoryListView(ListView):

    # model = Category
    http_method_names = ['get']
    queryset = Category.objects.filter(status=True)
    template_name = "web/category/list.html"
    context_object_name = "categories"


class CategroyGroupListView(TemplateResponseMixin, ContextMixin, View):
    http_method_names = ['get']
    template_name = 'web/category/detail.html'

    def get(self, request, *args, **kwargs):
        # log.info(kwargs)

        gid = kwargs.pop('gid', None)
        _page = request.GET.get('page', 1)
        category = Category.objects.get(pk = gid)
        sub_categories = Sub_Category.objects.filter(group=gid).values_list('id', flat=True)

        # log.info(sub_categories)

        _entity_list = Entity.objects.filter(category_id__in=list(sub_categories), status=Entity.selection).filter(buy_links__status=2)
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
            el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)

        context = {
            'entities':_entities,
            'user_entity_likes': el,
            'sub_category': category,
        }
        return self.render_to_response(context)

# TODO : already move this function to viewtools
# TODO : swith the viewtools version
def _get_paged_list(the_list, page_num=1, item_per_page=24):
    paginator = ExtentPaginator(the_list, item_per_page)
    try:
        _entities = paginator.page(page_num)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    return _entities

# TODO : already move this function to viewtools
# TODO : swith the viewtools version
def _get_entity_like_list(entity_list, request):
    el = []
    if request.user.is_authenticated():
        e = entity_list.object_list
        el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)
    return el


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


@require_GET
def detail(request, cid, template='web/category/detail.html'):
    _cid = cid
    _page = request.GET.get('page', 1)

    # _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _entity_list = Entity.objects.sort(category_id=cid, like=False)
    print _entity_list.query
    # _entity_list = Entity.objects.filter(status=Entity.selection, selection_entity__pub_time__lte=_refresh_datetime, category=_cid)\
    #                       .order_by('-selection_entity__pub_time').filter(buy_links__status=2)
    _sub_category = Sub_Category.objects.get(pk = _cid)
    _entities = _get_paged_list(_entity_list, _page, 24)
    el = _get_entity_like_list(_entities, request)

    return render_to_response(
        template,
        {
            'sub_category': _sub_category,
            'entities': _entities,
            'user_entity_likes': el,
            'sort_method': 'pub_time',
            'cid': _cid,
        },
        context_instance = RequestContext(request),
    )

@require_GET
def detail_like(request, cid , template='web/category/detail.html'):
    _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _cid = cid
    _page = request.GET.get('page',1)
    _entity_list = Entity.objects.sort(category_id=cid,like=True)
    # _entity_list = Entity.objects.filter(status=Entity.selection,selection_entity__pub_time__lte=_refresh_datetime , category=_cid, buy_links__status=2)\
    #                .annotate(lnumber=Count('likes'))\
    #                .order_by('-lnumber')
    _sub_category   = Sub_Category.objects.get(pk = _cid)
    _entities       = _get_paged_list(_entity_list,_page,24)
    _user_like_list = _get_entity_like_list(_entities, request)
    return render_to_response(
        template,
        {
            'sub_category' : _sub_category,
            'entities': _entities,
            'user_entity_likes' : _user_like_list,
            'sort_method': 'likes_count',
             'cid': _cid,
        },
        context_instance = RequestContext(request),
    )




__author__ = 'edison7500'