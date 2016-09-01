#encoding=utf-8
from pprint import  pprint
import types

from hashlib import md5
from urllib import urlencode

from django.core.urlresolvers import reverse, reverse_lazy

from apps.payment.basepay import BasePayment
from apps.payment.alipay.settings import alipay_settings
from apps.payment.alipay import sign_checker


class AliPayPayment(BasePayment):
    _GATEWAY = 'https://mapi.alipay.com/gateway.do?'

    @property
    def payment_url(self):
        # pprint(self.get_request_param())
        return self._GATEWAY + urlencode(self.get_request_param())

    def get_request_param(self):
        params = dict()
        params['service']           = 'create_direct_pay_by_user'
        # 获取配置文件
        params['partner']           = alipay_settings.ALIPAY_PARTNER
        params['seller_email']      = alipay_settings.ALIPAY_SELLER_EMAIL
        #urls
        params['return_url']        = self._host + reverse('alipay_return')
        params['notify_url']        = self._host + reverse('alipay_notify')
        params['_input_charset']    = alipay_settings.ALIPAY_INPUT_CHARSET
        params['show_url']          = alipay_settings.ALIPAY_SHOW_URL
        #业务参数
        params['out_trade_no']      = self._order.number
        params['subject']           = self._order.payment_subject
        params['payment_type']      = 1
        params['body']              = self._order.payment_body
        params['total_fee']         = self._order.order_total_value

        params['paymethod']         = 'directPay'
        params['defaultbank']       = ''
        # 扩展功能参数——防钓鱼
        params['anti_phishing_key'] = ''
        params['exter_invoke_ip']   = ''

        # 扩展功能参数——自定义参数
        params['buyer_email'] = ''
        params['extra_common_param'] = ''

        # 扩展功能参数——分润
        params['royalty_type'] = ''
        params['royalty_parameters'] = ''

        params, prestr = sign_checker.params_filter(params)
        params['sign'] = sign_checker.build_sign(prestr, alipay_settings.ALIPAY_KEY, alipay_settings.ALIPAY_SIGN_TYPE)
        params['sign_type'] = alipay_settings.ALIPAY_SIGN_TYPE
        return params






