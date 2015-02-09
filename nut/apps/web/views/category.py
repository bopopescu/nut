from django.shortcuts import render_to_response
from django.http import Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext
from django.views.generic import ListView
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from apps.core.models import Category, Sub_Category, Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage


from django.utils.log import getLogger
log = getLogger('django')



class CategoryListView(ListView):

    # model = Category
    http_method_names = ['get']
    queryset = Category.objects.filter(status=True)
    template_name = "web/category/list.html"
    context_object_name = "categories"


# class CategroyGroupListView(TemplateResponseMixin, ContextMixin, View):
#     http_method_names = ['get']
#     template_name = 'web/category/detail.html'
#
#     def get(self, request, *args, **kwargs):
#         # log.info(kwargs)
#         gid = kwargs.pop('gid', None)
#
#         sub_categories = Sub_Category.objects.filter(group=gid).values_list('id', flat=True)
#
#         # log.info(sub_categories)
#
#         entity_list = Entity.objects.filter(category_id__in=list(sub_categories), status=Entity.selection)
#
#         log.info(entity_list)
#
#         context = {
#             # 'entities':_entities,
#             # 'user_entity_likes': el,
#             # 'categories': _categories,
#         }
#         return self.render_to_response(context)


class CategroyGroupListView(ListView):
    http_method_names = ['get']
    template_name = 'web/category/detail.html'
    context_object_name = "entities"
    # paginator_class = ExtentPaginator
    page_kwarg = "page"
    paginate_by = 28

    def get_queryset(self):
        log.info(self.kwargs)
        self.gid = self.kwargs.pop('gid', None)
        sub_categories = Sub_Category.objects.filter(group=self.gid).values_list('id', flat=True)
        entity_list = Entity.objects.filter(category_id__in=list(sub_categories), status=Entity.selection)
        log.info(entity_list)

        return entity_list[:60]

    def get_context_data(self, **kwargs):
        context = super(CategroyGroupListView, self).get_context_data(**kwargs)
        category = Category.objects.get(pk = self.gid)
        context['sub_category'] = category
        return context
    #     self.con
    #     return

# @require_GET
# def list(request, template='web/category/list.html'):
#
#     _categories = Category.objects.filter(status=True)
#
#     return render_to_response(
#         template,
#         {
#             'categories': _categories,
#         },
#         context_instance = RequestContext(request),
#     )




# @require_GET
# def group(request, cid, template="web/category/group.html"):
#
#
#
#     return render_to_response(
#         template,
#         {
#
#         },
#         context_instance = RequestContext(request),
#     )

@require_GET
def detail(request, cid, template='web/category/detail.html'):
    _cid = cid
    _page = request.GET.get('page', 1)
    _entity_list = Entity.objects.filter(status=Entity.selection, category=_cid)
    _sub_category = Sub_Category.objects.get(pk = _cid)

    paginator = ExtentPaginator(_entity_list, 24)
    try:
        _entities = paginator.page(_page)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404

    el = []
    if request.user.is_authenticated():
        e = _entities.object_list
        el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)

    return render_to_response(
        template,
        {
            'sub_category': _sub_category,
            'entities': _entities,
            'user_entity_likes': el,
        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison7500'
