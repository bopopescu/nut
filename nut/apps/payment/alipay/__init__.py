#encoding=utf-8
from pprint import  pprint
import types

from hashlib import md5
from urllib import urlencode

from django.core.urlresolvers import reverse, reverse_lazy

from apps.payment.basepay import BasePayment

class alipay_settings:
    # ALIPAY_KEY = "ys06dn6fa1hrlgl37d3i8hbo14d6ody4"
    ALIPAY_KEY = "sij86zv335q7fb2k54iznoxg6s2z19g2"
    ALIPAY_INPUT_CHARSET = 'utf-8'
    # ALIPAY_PARTNER = '2088601343153581'
    ALIPAY_PARTNER = '2088511535586742'
    # ALIPAY_SELLER_EMAIL = 'guoku.com@gmail.com'
    ALIPAY_SELLER_EMAIL = 'hi@guoku.com'
    ALIPAY_SIGN_TYPE = 'MD5'
    # ALIPAY_RETURN_URL = 'http://h.guoku.com/payment/alipay/return/'
    # ALIPAY_NOTIFY_URL = 'http://h.guoku.com/payment/alipay/notify/'
    # ALIPAY_REFUND_NOTIFY_URL = 'http://h.guoku.com/payment/alipay/refund/notify/'
    ALIPAY_SHOW_URL = ''
    ALIPAY_TRANSPORT = 'https'

    @property
    def ALIPAY_NOTIFY_URL(self):
        return reverse_lazy('alipay_notify')

    @property
    def ALIPAY_RETURN_URL(self):
        return reverse_lazy('alipay_return')

    @property
    def ALIPAY_REFUND_NOTIFY_URL(self):
        return reverse_lazy('alipay_refund_notify')

class AliPayPayment(BasePayment):
    _GATEWAY = 'https://mapi.alipay.com/gateway.do?'

    @property
    def payment_url(self):
        pprint(self.get_request_param())
        return self._GATEWAY + urlencode(self.get_request_param())

    def get_request_param(self):
        params = dict()
        params['service']           = 'create_direct_pay_by_user'
        # 获取配置文件
        params['partner']           = alipay_settings.ALIPAY_PARTNER
        params['seller_email']      = alipay_settings.ALIPAY_SELLER_EMAIL
        params['return_url']        = alipay_settings.ALIPAY_RETURN_URL
        params['notify_url']        = alipay_settings.ALIPAY_NOTIFY_URL
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

        params, prestr = self.params_filter(params)

        params['sign'] = self.build_sign(prestr, alipay_settings.ALIPAY_KEY, alipay_settings.ALIPAY_SIGN_TYPE)
        params['sign_type'] = alipay_settings.ALIPAY_SIGN_TYPE
        return params


    def build_sign(self, prestr, key, sign_type = 'MD5'):
        if sign_type == 'MD5':
            return md5(prestr + key).hexdigest()
        return ''

    def params_filter(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = self.smart_str(k, alipay_settings.ALIPAY_INPUT_CHARSET)
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = self.smart_str(v, alipay_settings.ALIPAY_INPUT_CHARSET)
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr

    def smart_str(self, s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Returns a bytestring version of 's', encoded as specified in 'encoding'.

        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int)):
            return s
        if not isinstance(s, basestring):
            try:
                return str(s)
            except UnicodeEncodeError:
                if isinstance(s, Exception):
                    # An Exception subclass containing non-ASCII data that doesn't
                    # know how to print itself properly. We shouldn't raise a
                    # further exception.
                    return ' '.join([self.smart_str(arg, encoding, strings_only,
                            errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s





