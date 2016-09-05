from django.conf.urls import url, patterns
from apps.v4.views.orders.order import OrderListView

urlpatterns = patterns(
    'apps.v4.views.orders.order',
    url(r'^$', OrderListView.as_view(), name='v4_user_order_list')
)