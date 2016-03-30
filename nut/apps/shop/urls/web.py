from django.conf.urls import url, patterns

from apps.shop.views.web import SellerStoreListView

urlpatterns = patterns(
    '',
    url(r'^$', SellerStoreListView.as_view(), name='good_store')
)