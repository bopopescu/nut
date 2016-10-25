from django.conf.urls import url, patterns
from apps.offline_shop.views import OfflineShopDetailView

urlpatterns = patterns(
    '',
    url(r'^(?P<offline_shop_id>\d+)/$', OfflineShopDetailView.as_view(), name='web_offline_shop_detail')
)
