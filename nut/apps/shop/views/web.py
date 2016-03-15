from django.views.generic import ListView

from apps.core.models import GKUser
from apps.shop.models import StorePageBanners, StorePageRecommend
from apps.core.mixins.views import  FilterMixin, SortMixin
from apps.shop.models import Shop
class SellerStoreListView(FilterMixin, ListView):
    template_name = 'web/shop/sellers.html'
    model = GKUser
    context_object_name = 'sellers'
    def get_queryset(self):
        return GKUser.objects.authorized_seller()

    def filter_queryset(self, qs, filter_param):
        return qs

    def get_banners(self):
        return StorePageBanners.objects.filter(status=StorePageBanners.enabled)

    def get_recommends(self):
        return StorePageRecommend.objects.filter(status=StorePageRecommend.enabled)

    def get_storepage_message(self):
        return None

    def get_current_shop_type(self):
        return self.request.GET.get('shop_type', None)

    def get_current_shop_style(self):
        return self.request.GET.get('shop_style', None)


    def get_context_data(self, *args, **kwargs):
        context = super(SellerStoreListView, self).get_context_data(*args, **kwargs)
        context['banners'] = self.get_banners()
        context['recommends'] = self.get_recommends()
        context['messages'] = self.get_storepage_message()

        context['shop_type_filters'] = Shop.SHOP_TYPE_CHOICES
        context['shop_style_filters'] = Shop.SHOP_STYLE_CHOICES
        context['current_shop_type'] = self.get_current_shop_type()
        context['current_shop_style'] = self.get_current_shop_style()

        return context


    pass