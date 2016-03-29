from django.views.generic import  DetailView, ListView

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

    def get_queryset(self):
        pass


