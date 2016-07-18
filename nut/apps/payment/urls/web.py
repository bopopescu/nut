from django.conf.urls import url, patterns

from apps.payment.views.web import AlipayNotifyView , AlipayReturnView, AlipayRefoundNotify

urlpatterns = patterns(
    'apps.payment.views.web',
    url(r'^return/$', AlipayReturnView.as_view() , name="alipay_return"),
    url(r'^notify/$', AlipayNotifyView.as_view() , name="alipay_notify"),
    url(r'^refound_notify/$', AlipayRefoundNotify.as_view() , name="alipay_refund_notify"),
)