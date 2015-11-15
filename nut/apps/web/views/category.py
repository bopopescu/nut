from datetime import  datetime
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.views.generic import ListView, RedirectView
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

from apps.core.models import Category, Sub_Category, Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.log import getLogger
from apps.core.utils.http import JSONResponse


log = getLogger('django')


class CategoryListView(ListView):

    # model = Category
    http_method_names = ['get']
    queryset = Category.objects.filter(status=True)
    template_name = "web/category/list.html"
    context_object_name = "categories"


class CategoryGroupListView(TemplateResponseMixin, ContextMixin, View):
    http_method_names = ['get']
    template_name = 'web/category/detail.html'

    def get(self, request, *args, **kwargs):
        # log.info(kwargs)

        gid = kwargs.pop('gid', None)
        _page = request.GET.get('page', 1)
        category = Category.objects.get(pk=gid)
        sub_categories = Sub_Category.objects.filter(group=gid).values_list('id', flat=True)

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


from django.template import loader, RequestContext
from braces.views import JSONResponseMixin, AjaxResponseMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
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

    def get_queryset(self):
        cid = self.get_category_id()
        self.cid = cid
        sub_categories = Sub_Category.objects.filter(group=cid).values_list('id', flat=True)
        return Entity.objects.filter(category_id__in=list(sub_categories),
                                     status=Entity.selection).filter(buy_links__status=2)

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
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        cid = self.cid
        entities = context['page_obj']
        context['refresh_datetime'] = self.get_refresh_time()
        el = list()
        category = Category.objects.get(pk=cid)
        if self.request.user.is_authenticated():
            e = entities.object_list
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=list(
                                                        e.values_list(
                                                            'id',
                                                            flat=True))
                                                    ).using('slave')
        context['user_entity_likes'] = el
        context['entities'] = entities
        context['sub_category'] = category
        return context


@require_GET
def detail_like(request, cid , template='web/category/detail.html'):
    _cid = cid
    _page = request.GET.get('page',1)
    _entity_list = Entity.objects.sort(category_id=cid,like=True).exclude(selection_entity__is_published=False)
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

