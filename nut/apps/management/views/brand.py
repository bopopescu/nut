# from django.shortcuts import render_to_response
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from apps.core.models import Brand
# import random
# from django.db.models import Count
# from apps.core.models import Entity, Entity_Like, Sub_Category
from django.utils.log import getLogger

log = getLogger('django')



class BrandListView(TemplateResponseMixin, ContextMixin, View):
    template_name = "management/brand/list.html"

    def get(self, request):
        _brand_list = Brand.objects.all()
        context = {
            'brands':_brand_list,
        }
        return self.render_to_response(context)


__author__ = 'edison'
