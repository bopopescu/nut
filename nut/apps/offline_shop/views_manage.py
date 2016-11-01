from django.views.generic import ListView

from apps.offline_shop.models import Offline_Shop_Info


class OfflineShopListView(ListView):
    template_name = 'management/offline_shop/list.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Offline_Shop_Info.objects.active_offline_shops()
