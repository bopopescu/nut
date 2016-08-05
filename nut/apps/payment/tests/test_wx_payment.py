from pprint import pprint
from apps.order.tests import  DBTestBase
from apps.payment.weixinpay import WXPayment

from apps.payment.weixinpay.config import WX_APPID, WX_APPSEC, WX_MCH_ID
from xml.etree import cElementTree as ET
class WX_Payment_Test(DBTestBase):
    def setUp(self):
        super(WX_Payment_Test, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size':165
        })
        self.sku1.stock = 5
        self.sku1.origin_price = 0.02
        self.sku1.promo_price = 0.01
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color':'black',
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

    def test_price(self):
        self.assertEqual(self.order.order_total_value,0.03)

    def test_appid(self):
        wxpayment = WXPayment(self.order)
        params = wxpayment.get_request_params()
        self.assertEqual(params['appid'],WX_APPID)
        self.assertEqual(int(params['total_fee']), 3)
        self.assertEqual(params['norify_url'] , 'http://www.guoku.com/payment/wxpay/notify/')


    def test_generate_xml_string(self):
        params={'name':'an','age':'19'}
        root = ET.Element('xml')
        for k,v in params.iteritems():
            ET.SubElement(root, k).text=v
        str = ET.tostring(root, encoding='utf8', method='xml')
        self.assertIsInstance(str, basestring)

    def test_xml_generate(self):
        wxpayment = WXPayment(self.order)
        str = wxpayment.get_request_xml_string()
        self.assertEqual('wx59118ccde8270caa' in str , True)

    def test_request_qr_code(self):
        import requests
        wxpayment = WXPayment(self.order)
        response = requests.post(WXPayment._GATEWAY,
                                 data=wxpayment.get_request_xml_string(),
                                 headers={'Content-Type':'application/xml'}
                                )

        # pprint(response)
        self.assertEqual(response.url , wxpayment._GATEWAY)
        # url = wxpayment.parse_payment_url(response)
        #
        pprint(response.text)
        pprint(response.content)
        response.encoding='utf-8'
        pprint(response.text)
        root = ET.fromstring(response.text)
        pprint(root)

        # self.assertEqual(url, 'not fit')






