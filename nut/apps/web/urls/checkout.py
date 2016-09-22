
from django.conf.urls import url, patterns
from apps.web.views.checkout import CheckoutOrderListView, CheckDeskPayView,\
                                    CheckDeskAllOrderListView, CheckDeskOrderStatisticView,\
                                    CheckoutOrderDetailView
urlpatterns = patterns(
    'apps.web.views.checkout',
    url(r'^$', CheckDeskAllOrderListView.as_view(), name='checkout_index'),
    url(r'^statistic/$', CheckDeskOrderStatisticView.as_view(), name='checkdesk_order_statistic'),
    url(r'^order_list/$', CheckoutOrderListView.as_view(), name='checkout_order_list'),
    url(r'^orders/(?P<order_number>\d+)/$', CheckoutOrderDetailView.as_view(), name='checkout_order_detail'),

    url(r'^order_list/pay/$', CheckDeskPayView.as_view(), name="checkout_done")
)