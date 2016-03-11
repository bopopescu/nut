from django.views.generic import  DetailView, ListView

from apps.core.models import Brand

# TODO Brand front end view


class BrandListView(ListView):
    model = Brand
    template_name = 'web/brand/list.html'


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'web/brand/detail.html'
    context_object_name = 'brand'