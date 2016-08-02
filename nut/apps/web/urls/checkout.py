
from django.conf.urls import url, patterns
from apps.web.views.checkout import MyOrderListView,MyOrderDetailView,MyOrderDeleteView

urlpatterns = patterns(
    'apps.web.views.checkout',
    url(r'^myorder/(?P<order_number>\d+)/detail/$', MyOrderDetailView.as_view(), name='my_order_detail_management'),
    url(r'^myorder/(?P<order_number>\d+)/delete/$',MyOrderDeleteView.as_view(),name='my_order_delete_management'),
    url(r'^order_list/$', MyOrderListView.as_view(), name='web_my_order_list'))