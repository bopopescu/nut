from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.core.models import Brand

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
        brand_pk = self.kwargs.get('pk')
        brand = get_object_or_404(Brand, pk=brand_pk)
        sqs = brand.entities

        return sqs

    def get_context_data(self, **kwargs):
        brand_pk = self.kwargs.get('pk')
        context = super(BrandDetailView, self).get_context_data(**kwargs)
        context['brand'] = get_object_or_404(Brand, pk=brand_pk)
        return context

