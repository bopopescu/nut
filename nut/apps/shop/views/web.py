from django.views.generic import ListView

from apps.core.models import GKUser
from apps.shop.models import StorePageBanners, StorePageRecommend
from apps.core.mixins.views import  FilterMixin, SortMixin

class SellerStoreListView(FilterMixin, ListView):
    template_name = 'web/shop/sellers.html'
    model = GKUser

    def get_banners(self):
        return StorePageBanners.objects.filter(status=StorePageBanners.enabled)

    def get_recommends(self):
        return StorePageRecommend.objects.filter(status=StorePageRecommend.enabled)


    def get_storepage_message(self):
        return None

    def get_context_data(self, *args, **kwargs):
        context = super(SellerStoreListView, self).get_context_data(*args, **kwargs)
        context['banners'] = self.get_banners()
        context['recommends'] = self.get_recommends()
        context['messages'] = self.get_storepage_message()

        return context


    pass