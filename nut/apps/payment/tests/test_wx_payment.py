# -*- coding: UTF-8 -*-
import requests
from django.conf import settings
from pprint import pprint
from apps.order.tests import DBTestBase
from apps.payment.weixinpay import WXPayment

from apps.payment.weixinpay.config import WX_APPID
from xml.etree import cElementTree as ET

site_host = getattr(settings, 'SITE_HOST', None)


class WX_Payment_Test(DBTestBase):
    def setUp(self):
        super(WX_Payment_Test, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })
        self.sku1.stock = 5
        self.sku1.origin_price = 0.02
        self.sku1.promo_price = 0.01
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color': 'black',
            'size': 128
        })
        self.sku2.stock = 5
        self.sku2.origin_price = 0.03
        self.sku2.promo_price = 0.01
        self.sku2.save()

        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.add_sku_to_cart(self.sku2)
        self.the_user.add_sku_to_cart(self.sku2)

        self.order = self.the_user.checkout()

        self.the_user.add_sku_to_cart(self.sku2)
        self.order2 = self.the_user.checkout()

    def test_price(self):
        self.assertEqual(self.order.order_total_value, 0.03)

    def test_appid(self):
        wxpayment = WXPayment(self.order)
        params = wxpayment.get_request_params()
        self.assertEqual(params['appid'], WX_APPID)
        self.assertEqual(int(params['total_fee']), 3)
        self.assertEqual(params['notify_url'], '%s/payment/wxpay/notify/' % site_host)

    def test_generate_xml_string(self):
        params = {'name': 'an', 'age': '19'}
        root = ET.Element('xml')
        for k, v in params.iteritems():
            ET.SubElement(root, k).text = v
        theStr = ET.tostring(root, encoding='utf8', method='xml')
        self.assertIsInstance(theStr, basestring)

    def test_xml_generate(self):
        wxpayment = WXPayment(self.order)
        theStr = wxpayment.get_request_xml_string()
        print(theStr)
        self.assertEqual('wx59118ccde8270caa' in theStr, True)

    def test_xml_post(self):
        # make sure wx payment api work
        # api key is right etc ...

        wxpayment = WXPayment(self.order)
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(wxpayment._GATEWAY,
                                 data=wxpayment.get_request_xml_string(),
                                 headers=headers)
        response.encoding = 'utf-8'
        pprint(response.text)
        from django.utils.encoding import smart_str, smart_unicode
        raw_str = smart_str(response.text)
        root = ET.fromstring(raw_str)
        msg = {}
        if root.tag == 'xml':
            for child in root:
                msg[child.tag] = smart_unicode(child.text)
        pprint(msg)
        print(msg['return_msg'].encode('utf8'))
        self.assertEqual('weixin://wxpay/' in raw_str, True)

    def test_xml_post_resposne_sign(self):
        # make sure the response is returning from wx
        # make sure the sign checking algorithm is right
        wxpayment = WXPayment(self.order)
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(wxpayment._GATEWAY,
                                 data=wxpayment.get_request_xml_string(),
                                 headers=headers)
        response.encoding = 'utf-8'
        pprint(response.text)
        from django.utils.encoding import smart_str, smart_unicode
        raw_str = smart_str(response.text)
        root = ET.fromstring(raw_str)
        msg = {}
        if root.tag == 'xml':
            for child in root:
                msg[child.tag] = smart_unicode(child.text)
        self.assertEqual(wxpayment._parser.check_wx_response_sign(response), True)

    def test_get_wx_pay_url(self):
        wxpayment = WXPayment(self.order)
        wx_pay_url = wxpayment.get_payment_qrcode_url()
        print('-'*80)
        pprint(wx_pay_url)
        self.assertEqual('weixin://wxpay/' in wx_pay_url, True)

    def test_get_wx_prepay_id(self):
        wxpayment = WXPayment(self.order)
        prepay_id = wxpayment.get_prepay_id()
        self.assertIsNotNone(prepay_id)
        self.assertIsInstance(prepay_id, unicode)
        self.assertLessEqual(3, len(prepay_id))
