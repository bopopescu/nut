import xml.etree.cElementTree as ET

from django.http import HttpResponse
from django.views.generic import FormView, View, TemplateView

from apps.payment.weixinpay.parser import WXResponseParser
from apps.payment.weixinpay.handler import WXPaymentNotifyHanlder
from django.utils.log import getLogger
log = getLogger('django')



class AlipayReturnView(FormView):
    pass

class AlipayNotifyView(FormView):
    pass

class AlipayRefoundNotify(FormView):
    pass

class WXpayReturnView(FormView):
    pass

class WXPayNotifyView(View):
    template_name = 'payment/notify.html'

    def post(self, *args, **kwargs):
        #only return False when
        log.error('weixin notify here')
        parser = WXResponseParser()
        if not parser.check_wx_request_sign(self.request):
            log.warning('wx notify sign fail')
            result_xml_str = self.build_xml_return_str({
                'return_code': 'FAIL',
                'msg':'sign failed'
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

