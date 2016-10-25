from django.views.generic import DetailView
from apps.offline_shop.models import Offline_Shop_Info


class OfflineShopDetailView(DetailView):
    template_name = 'web/offline_shop/offline_detail.html'
    pk_url_kwarg = 'offline_shop_id'
    model = Offline_Shop_Info
    context_object_name = 'offline_shop'

    def get_context_data(self,**kwargs):
        context_data = super(OfflineShopDetailView, self).get_context_data(**kwargs)
        context_data['current_user'] = context_data['object'].shop_owner

        return context_data
