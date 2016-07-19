from django.conf.urls import url, patterns
from apps.order.views.web.order import UserOrderListView, UserOrderView
urlpatterns = patterns(
    'apps.order.views.web.cart',
    url(r'^$', UserOrderListView.as_view(), name='web_user_order_list'),
    url(r'^(?P<pk>\d+)/$', UserOrderView.as_view(), name='web_user_order'),
)