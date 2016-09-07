from django.conf.urls import url, patterns
from apps.v4.views.orders.order import OrderListView, WeChatPaymentView

urlpatterns = patterns(
    'apps.v4.views.orders.order',
    url(r'^$', OrderListView.as_view(), name='v4_user_order_list'),

    url(r'payment/weixin/(?P<order_id>\d+)/$', WeChatPaymentView.as_view(), name='v4_wechat_payment_url'),
)