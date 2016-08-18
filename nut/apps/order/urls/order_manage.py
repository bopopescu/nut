from django.conf.urls import url, patterns
from apps.order.views.management.order import OrderListView,SoldEntityListView,ManagementOrderDetailView

urlpatterns = patterns(
    'apps.order.views.management.order',
    url(r'^order_list/$',OrderListView.as_view(),name='management_order_list'),
    url(r'^sold_entity/$',SoldEntityListView.as_view(),name='management_sold_list'),
    url(r'^(?P<order_number>\d+)/detail/$',ManagementOrderDetailView.as_view(),name='management_order_detail')
)