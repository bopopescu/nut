from django.conf.urls import url, patterns

from apps.payment.views.web import AlipayNotifyView, AlipayReturnView, AlipayRefundNotify,\
                                   WXpayReturnView, WXPayNotifyView, WXpayRefoundView, AlipayPayFailView

urlpatterns = patterns(
    'apps.payment.views.web',
    url(r'^alipay/return/$', AlipayReturnView.as_view(), name="alipay_return"),
    url(r'^alipay/notify/$', AlipayNotifyView.as_view(), name="alipay_notify"),
    url(r'^alipay/refound_notify/$', AlipayRefundNotify.as_view(), name="alipay_refound_notify"),
    url(r'^alipay/fail/$', AlipayPayFailView.as_view(), name="alipay_pay_fail"),

    url(r'^wxpay/return/$', WXpayReturnView.as_view() , name="wxpay_return"),
    url(r'^wxpay/notify/$', WXPayNotifyView.as_view(), name="wxpay_notify"),
    url(r'^wxpay/refound_notify/$', WXpayRefoundView.as_view() , name="wxpay_refound_notify"),
)