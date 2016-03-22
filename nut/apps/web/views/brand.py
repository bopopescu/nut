from django.http import Http404
from django.views.generic import ListView
from haystack.query import SearchQuerySet
from django.shortcuts import get_object_or_404
from apps.core.models import Brand, Entity

# TODO Brand front end view


class BrandListView(ListView):
    model = Brand
    template_name = 'web/brand/list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.all()


class BrandDetailView(ListView):
    template_name = 'web/brand/detail.html'
    paginate_by = 40
    context_object_name = 'entities'

    def get_queryset(self):
        brand_pk= self.kwargs.pop('pk')
        brand = get_object_or_404(Brand, pk=brand_pk)
        sqs = SearchQuerySet().models(Entity).filter(brand=brand.name)

        return sqs

