from django.conf.urls import url, patterns
from apps.offline_shop.views_manage import OfflineShopListView

urlpatterns = patterns('',
                       url(r'^$', OfflineShopListView.as_view(), name='management_offline_shop_list')
                       )
