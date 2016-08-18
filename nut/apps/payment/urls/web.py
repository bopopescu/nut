from django.conf.urls import url, patterns

from apps.payment.views.web import AlipayNotifyView , AlipayReturnView, AlipayRefoundNotify,\
                                   WXpayReturnView, WXPayNotifyView,WXpayRefoundView


urlpatterns = patterns(
    'apps.payment.views.web',
    url(r'^alipay/return/$', AlipayReturnView.as_view() , name="alipay_return"),
    url(r'^alipay/notify/$', AlipayNotifyView.as_view() , name="alipay_notify"),
    url(r'^alipay/refound_notify/$', AlipayRefoundNotify.as_view() , name="alipay_refound_notify"),
    url(r'^wxpay/return/$', WXpayReturnView.as_view() , name="wxpay_return"),
    url(r'^wxpay/notify/$', WXPayNotifyView.as_view(), name="wxpay_notify"),
    url(r'^wxpay/refound_notify/$', WXpayRefoundView.as_view() , name="wxpay_refound_notify"),
)