
from django.conf.urls import url, patterns
from apps.web.views.checkout import SellerOrderListView,SellerOrderDetailView,SellerOrderDeleteView,IndexView

urlpatterns = patterns(
    'apps.web.views.checkout',
    url(r'^$',IndexView.as_view(),name='checkout_index'),
    url(r'^order/(?P<order_number>\d+)/detail/$', SellerOrderDetailView.as_view(), name='checkout_order_detail_management'),
    url(r'^order/(?P<order_number>\d+)/delete/$',SellerOrderDeleteView.as_view(),name='checkout_order_delete_management'),
    url(r'^order_list/$', SellerOrderListView.as_view(), name='checkout_order_list')
)