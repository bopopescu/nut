# from django.shortcuts import render_to_response
# from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

from django.http import Http404
from apps.core.models import Brand
# import random
# from django.db.models import Count
from apps.core.models import Entity
from apps.core.views import BaseListView
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage

from django.utils.log import getLogger

log = getLogger('django')

class BrandStatView(BaseListView):
    template_name = "management/brand/stat.html"

    def get_queryset(self):

        entities_stat = Entity.objects.raw("select id, brand, count(*) as b  from core_entity where brand !='' and status != -1  group by brand ORDER BY b DESC")
        return entities_stat

    def get(self, request):

        _brand_stat_list = self.get_queryset()
        page = request.GET.get('page', 1)

        paginator = ExtentPaginator(list(_brand_stat_list), 30)

        try:
            _brand_stat = paginator.page(page)
        except InvalidPage:
            _brand_stat = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'brand_stat': _brand_stat,
        }

        return self.render_to_response(context)

class BrandListView(BaseListView):
    template_name = "management/brand/list.html"
    # queryset = Brand.objects.all()

    def get_queryset(self):

        return Brand.objects.all()

    def get(self, request):
        _brand_list = self.get_queryset()
        page = request.GET.get('page', 1)

        paginator = ExtentPaginator(_brand_list, 30)

        try:
            _banrds = paginator.page(page)
        except InvalidPage:
            _banrds = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'brands':_banrds,
        }
        return self.render_to_response(context)


class BrandEntityListView(BaseListView):
    template_name = 'management/brand/entities.html'

    def get_queryset(self, **kwargs):
        name = kwargs.pop('brand_name')
        return Entity.objects.filter(brand__contains=name)

    def get(self, request, brand):
        _entity_list = self.get_queryset(brand_name=brand)
        page = request.GET.get('page', 1)

        paginator = ExtentPaginator(_entity_list, 30)

        try:
            _entities = paginator.page(page)
        except InvalidPage:
            _entities = paginator.page(1)
        except EmptyPage:
            raise Http404

        context = {
            'brand': brand,
            'entities': _entities,
        }
        return self.render_to_response(context)

__author__ = 'edison'
