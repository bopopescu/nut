import json
import types
import xml.etree.cElementTree as ET
from hashlib import md5

import datetime
from braces.views import CsrfExemptMixin

from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import FormView, View, TemplateView
from django.utils.log import getLogger


from apps.payment.alipay import alipay_settings
from apps.payment.weixinpay.parser import WXResponseParser
from apps.payment.weixinpay.handler import WXPaymentNotifyHanlder

from apps.order.models import Order
from apps.payment.alipay import sign_checker
from apps.payment.models import PaymentLog

log = getLogger('django')


class AlipayReturnView(TemplateView):
    def get(self, *args, **kwargs):
        # if self.check_sign() and self.check_payment_data():
        #     self.handle_pay_success()
        # through return result , only depend on notify
        return redirect('web_user_order', pk=self.get_order().pk)
        # else:
            # return redirect('alipay_pay_fail')

    def get_order(self):
        # TODO , cache order for later use !
        params = self.get_params()
        number = params.get('out_trade_no')
        return Order.objects.get(number=number)

    def check_sign(self):
        log.info('----- check sign ----')
        log.info(sign_checker.check_sign(self.get_params()))
        log.info('----- check sign end ----')
        return sign_checker.check_sign(self.get_params())

    def get_params(self):
        return self.request.GET

    def check_payment_data(self):
        return self.check_alipay_data() and self.check_order_price()

    def check_alipay_data(self):
        params = self.get_params()
        result = (params.get('sign_type') == 'MD5' and
                 (params.get('trade_status') == 'TRADE_FINISHED' or params.get('trade_status') == 'TRADE_SUCCESS'))

        log.info('------- check alipay data ---')
        log.info(result)
        log.info('------- check alipay data end ----')
        return result


    def check_order_price(self):
        params = self.get_params()
        order_number = params.get('out_trade_no')
        total_fee = params.get('total_fee')
        order = Order.objects.get(number=order_number)
        if order is None:
            return False
        result = order.order_total_value == float(total_fee)
        log.info('------- check order price  ---')
        log.info(result)
        log.info('------- check order price  ----')
        return result

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

    def write_alipay_log(self,):
        _order = self.get_order()
        _plog, created = PaymentLog.objects.get_or_create(
            order=_order,
            payment_source=PaymentLog.ali_pay,
            payment_status=PaymentLog.paid,
        )

        if created:
            _plog.payment_notify_info = json.dumps(self.get_params())
            _plog.pay_time = datetime.datetime.now()
            _plog.save()
            log.info('alipay payment log created')


class AlipayPayFailView(View):
    def get(self, *args, **kwargs):
        return HttpResponse(content='alipay pay failed', status=200)


class AlipayNotifyView(CsrfExemptMixin, AlipayReturnView):
    template_name = 'payment/notify.html'

    def get(self, *args, **kwargs):
        log.info('aliay notify should not use get method')
        return self.render_to_response({
            'result': 'get not accepted'
        })

    def get_params(self):
        return self.request.POST

    def post(self, *args, **kwargs):
        if self.check_sign() and self.check_payment_data():
            log.info('check notify data ok !!')
            self.handle_pay_success()
            return self.render_to_response({
                'result': 'success'
            })
        else:
            log.info('check notify data fail!!')
            log.info('----------')
            log.info(self.get_params())
            # TODO : testing , change following to success after test is success
            return self.render_to_response({
                'result': 'fail'
            })


class AlipayRefundNotify(FormView):
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



class WXpayRefundView(FormView):

    pass

