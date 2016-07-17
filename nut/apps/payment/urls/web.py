from django.conf.urls import url, patterns

from apps.payment.views.web import AlipayNotifyView , AlipayReturnView

urlpatterns = patterns(
    'apps.payment.views.web',
    url(r'^return/$', AlipayReturnView.as_view() , name="alipay_return"),
    url(r'^notify/$', AlipayNotifyView.as_view() , name="alipay_notify"),
)