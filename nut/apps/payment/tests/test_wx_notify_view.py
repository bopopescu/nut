from pprint import pprint

from django.core.urlresolvers import reverse
from django.test import  TestCase, RequestFactory
from apps.payment.views.web import WXPayNotifyView

from apps.payment.weixinpay.parser import WXResponseParser
from apps.order.tests import DBTestBase


class WXNotifyParserTest(DBTestBase):
    def setUp(self):
        super(WXNotifyParserTest,self).setUp()
        self.factory = RequestFactory()
        self.request_url = reverse('wxpay_notify')
        self.data =  '<xml></xml>'

    def test_notify_request_view_return_fail(self):
        request = self.factory.post(self.request_url, self.data, 'text/xml')
        response = WXPayNotifyView.as_view()(request)
        pprint('******')
        pprint(dir(response))
        pprint(response.content)
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers.get('content-type'), ('Content-Type', 'text/xml'))
        self.assertEqual('FAIL' in response.content, True)
        self.assertEqual('sign failed' in response.content, True)






