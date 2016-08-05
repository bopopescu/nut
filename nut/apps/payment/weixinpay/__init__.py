import  random, string
from pprint import pprint
from urllib import urlencode
from hashlib import md5
import  requests
import xml.etree.cElementTree as ET

from django.core.urlresolvers import reverse

from apps.payment.basepay import BasePayment
from apps.payment.weixinpay.config import WX_APPID, WX_APPSEC, WX_MCH_ID
from apps.payment.exceptions import PaymentException

class WXPayment(BasePayment):
    _GATEWAY = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    def get_payment_qrcode_url(self):
        headers = {'Content-Type':'application/xml'}
        response = requests.post(self._GATEWAY,
                                 data=self.get_request_xml_string(),
                                 headers=headers)
        return self.parse_payment_url(response)

    def parse_payment_url(self, response):

        if self.check_wx_response_sign(response) is not True:
            raise PaymentException('wx return sign fail')

        e = ET.parse(response.text).get_root()
        if getattr(e, 'return_code') == 'FAIL':
            raise PaymentException('wx payment api interno error %s'
                                   %getattr(e,'return_msg'))

        if getattr(e, 'result_code') == 'FAIL':
            raise PaymentException('wx payment get qrcode fail %s'
                                   %getattr(e,'err_code_des'))

        elif getattr(e, 'result_code') == 'SUCCESS':
            return getattr(e, 'code_url')

        else:
            raise PaymentException('unkown error')


    def check_wx_response_sign(self, response):
        # todo check wx response xml sign
        params = self.parse_string_xml_to_dic(response.text)
        sign = params.pop('sign', None)
        params, prestr = self.params_filter(params)
        check_sign = self.build_sigh(prestr,WX_APPSEC)
        return sign == check_sign

    def parse_string_xml_to_dic(self, xml_string):
        root  = ET.fromstring(xml_string)
        params = dict()
        for child in root :
            params[child.tag]=child.text
        return params

    def get_request_xml_string(self):
        root = ET.Element('xml')
        for k , v in self.get_request_params().iteritems():
            ET.SubElement(root, k).text = v
        return ET.tostring(root, encoding='utf8', method='xml')

    def get_rd_string(self, length=32):
        return ''.join(random.choice(string.lowercase) for i in range(length))


    def get_request_params(self):
        params = dict()
        params['appid'] = WX_APPID
        params['mch_id'] = WX_MCH_ID
        params['nonce_str'] = self.get_rd_string()
        params['body'] = self._order.payment_body
        params['out_trade_no'] = self._order.number
        params['total_fee'] = self.get_wx_order_total_fee()
        params['spbill_create_ip'] = self.get_spbill_ip()
        params['norify_url'] = self._host + self.notify_url
        params['trad_type'] = 'NATIVE'

        params, prestr = self.params_filter(params)
        params['sign'] = self.build_sign(prestr,WX_APPSEC)
        return params

    def build_sign(self, prestr, app_sec):
        signStringTemp = "prestr&key=%s"%app_sec
        return md5(signStringTemp).hexdigest().upper()

    def get_wx_order_total_fee(self):
        # https://pay.weixin.qq.com/wiki/doc/api/native.php?chapter=4_2
        # value is cent , not dollar
        return int(self._order.order_total_value * 100)

    @property
    def notify_url(self):
        return reverse('wxpay_notify')
    def payment_url(self):
        return self._GATEWAY + urlencode(self.get_request_param())


    def get_spbill_ip(self):
        return '114.113.154.46'

    def get_signed_params(self):
        pass





