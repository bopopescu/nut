from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.core.extend.paginator import ExtentPaginator
from apps.shop.models import StorePageBanners

class StoreBannerListView(ListView):
    template_name = 'management/shop/Store_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  StorePageBanners
    context_object_name = 'banners'
    def get_queryset(self):
        return StorePageBanners.objects.all()


class StoreBannerCreateView(CreateView):
    model = StorePageBanners
    template_name = 'management/shop/edit.html'

class StoreBannerUpdateView(UpdateView):
    pass

class StoreBannerDeleteView(DeleteView):
    pass

class StoreIndexView(ListView):
    pass