import types
import xml.etree.cElementTree as ET
from hashlib import md5
from braces.views import CsrfExemptMixin

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, View, TemplateView
from django.utils.log import getLogger


from apps.payment.alipay import alipay_settings
from apps.payment.weixinpay.parser import WXResponseParser
from apps.payment.weixinpay.handler import WXPaymentNotifyHanlder

from apps.order.models import Order

log = getLogger('django')


class SignChecker(object):

    @staticmethod
    def smart_str(cls, s, encoding='utf-8', strings_only=False, errors='strict'):
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
                    return ' '.join([cls.smart_str(arg, encoding, strings_only,
                            errors) for arg in s])
                return unicode(s).encode(encoding, errors)
        elif isinstance(s, unicode):
            return s.encode(encoding, errors)
        elif s and encoding != 'utf-8':
            return s.decode('utf-8', errors).encode(encoding, errors)
        else:
            return s

    @staticmethod
    def params_filter(cls, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = cls.smart_str(k)
            if k not in ('sign','sign_type') and v != '':
                newparams[k] = cls.smart_str(v)
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr

    @staticmethod
    def build_sign(cls, prestr, key, sign_type = 'MD5'):
        if sign_type == 'MD5':
            return md5(prestr + key).hexdigest()
        return ''

    @staticmethod
    def get_sign_from_param(cls, params):
        params, prestr = cls.params_filter(params)
        return cls.build_sign(prestr, alipay_settings.ALIPAY_KEY)

    @staticmethod
    def check_sign(cls, params):
        return params.get('sign', None) == cls.get_sign_from_params(params)
    

class AlipayReturnView(View):
    def get(self, *args, **kwargs):
        if self.check_sign() and self.check_payment_data():
            self.handle_pay_success()
            return redirect('web_user_order', pk=self.get_order().pk)
        else:
            return redirect('alipay_pay_fail')

        pass

    def get_order(self):
        # TODO , cache order for later use !
        params = self.get_params()
        number = params.get('out_trade_no')
        return Order.objects.get(number=number)



    def check_sign(self):
        return SignChecker.check_sign(self.get_params())

    def get_params(self):
        return self.request.GET

    def check_payment_data(self):
        return self.check_alipay_data() and self.check_order_price()

    def check_alipay_data(self):
        params = self.get_params()
        return (params.get('is_success') == 'T' and
                params.get('sign_type') == 'MD5' and
                (params.get('trade_status') == 'TRADE_FINISHED' or params.get('trade_status') == 'TRADE_SUCCESS'))

    def check_order_price(self):
        params = self.get_params()
        order_number = params.get('out_trade_no')
        total_fee = params.get('total_fee')
        order = Order.objects.get(number=order_number)
        if order is None:
            return False
        return order.order_total_value == float(total_fee)

    def handle_pay_success(self):
        params = self.get_params()
        order_number = params.get('out_trade_no')
        try:
            order = Order.objects.get(number=order_number)
            order.set_paid()
            self.write_alipay_log()
        except Order.DoesNotExist:
            pass
        except Order.MultipleObjectsReturned:
            pass
        except Exception :
            pass

    def write_alipay_log(self):
        pass


class AlipayPayFailView(View):
    def get(self):
        return 'alipay pay failed'
    pass


class AlipayNotifyView(FormView):
    pass


class AlipayRefoundNotify(FormView):
    pass


class WXpayReturnView(FormView):
    pass


class WXPayNotifyView(CsrfExemptMixin, View):
    template_name = 'payment/notify.html'

    def post(self, *args, **kwargs):
        # only return False when
        # log.error('weixin notify here')
        parser = WXResponseParser()
        if not parser.check_wx_request_sign(self.request):
            log.warning('wx notify sign fail')
            result_xml_str = self.build_xml_return_str({
                'return_code': 'FAIL',
                'msg': 'sign failed'
            })
            return HttpResponse(result_xml_str, content_type='text/xml')
        else:
            pay_dic = parser.parse_xml_request_to_dic(self.request)
            WXPaymentNotifyHanlder(pay_dic).handle_notify()
            result_xml_str =  self.build_xml_return_str({
                'return_code':'SUCCESS'
            })
            return HttpResponse(result_xml_str, content_type='text/xml')


    def get_order_from_result(self):
        raise NotImplemented()
        pass



    def build_xml_return_str(self, result):
        root = ET.Element('xml')
        for k,v in result.iteritems():
            ET.SubElement(root, k).text = v
        return ET.tostring(root,encoding='utf8', method='xml')



class WXpayRefoundView(FormView):

    pass

