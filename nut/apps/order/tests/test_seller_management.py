from pprint import pprint

from django.core.urlresolvers import reverse
from django.test import  TestCase, RequestFactory
from apps.web.views.checkout import AllOrderListView,SellerOrderListView,CheckDeskPayView
from apps.order.views.management.order import OrderListView,SoldEntityListView,ManagementOrderDetailView
from apps.web.views.seller_management import SellerManagement,QrcodeListView,SellerManagementAddEntity,SellerEntitySKUCreateView,SellerManagementEntitySave,\
                                             SKUStatusChangeView,SKUListView,SKUCreateView,SKUUpdateView,SKUDeleteView,\
                                             OrderDetailView,SellerManagementOrders,SellerManagementSkuSave,SellerManagementSoldEntityList,SellerManagementFinancialReport
from core.models import GKUser
from order.models import Order
from order.tests import DBTestBase



class CheckoutViewTest(DBTestBase):
    def setUp(self):
        super(CheckoutViewTest,self).setUp()
        self.factory = RequestFactory()
        self.data =  ''
        self.user=self.the_user
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })

        self.sku2 = self.entity.add_sku({
            'color': 'black',
            'size': 128
        })
        self.sku1.stock = 2432
        self.sku2.stock = 2423
        self.user.add_sku_to_cart(self.sku1)
        self.user.add_sku_to_cart(self.sku2)
        self.new_order = self.user.checkout()
    def test_all_order_list_view(self):
        request_url = reverse('checkout_index')
        request = self.factory.get(request_url, self.data)
        request.user=self.user
        response = AllOrderListView.as_view()(request)
        pprint('******')
        pprint('test AllOrderListView...')
        pprint(dir(response))
#        pprint(response.content)
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_seller_order_list_view(self):
        request_url=reverse('checkout_order_list')
        request = self.factory.get(request_url,self.data)
        request.user=self.user
        response=SellerOrderListView.as_view()(request)
        pprint('******')
        pprint('test SellerOrderListView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code,200)

    def test_check_desk_pay_view(self):
        request_url=reverse('checkout_done')
        id=self.new_order.id
        request=self.factory.post(request_url,data={'order_id':id})
        response=CheckDeskPayView.as_view()(request)
        pprint('******')
        pprint('test CheckDeskPayView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

class  ManagementOrderViewTest(DBTestBase):
    def setUp(self):
        super(ManagementOrderViewTest,self).setUp()
        self.factory = RequestFactory()
        self.data=''
        self.user=self.the_user
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })

        self.sku2 = self.entity.add_sku({
            'color': 'black',
            'size': 128
        })
        self.sku1.stock = 2432
        self.sku2.stock = 2423
        self.user.add_sku_to_cart(self.sku1)
        self.user.add_sku_to_cart(self.sku2)
        self.new_order=self.user.checkout()
    def test_order_list_view(self):
        request_url=reverse('management_order_list')
        request = self.factory.get(request_url,self.data)
        request.user = self.user
        response = OrderListView.as_view()(request)
        pprint("******")
        pprint('test OrderListView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code,200)
    def test_sold_entity_list_view(self):
        request_url = reverse('management_sold_list')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SoldEntityListView.as_view()(request)
        pprint("******")
        pprint('test SoldEntityListView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_management_order_detail_view(self):
        order_number=self.new_order.id
        request_url = reverse('management_order_detail', args=[order_number])
        request=self.factory.get(request_url,self.data)
        request.user=self.user
        response=ManagementOrderDetailView.as_view()(request)
        pprint('******')
        pprint('test ManagementOrderDetaolView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code,200)

class SellerManagementViewTest(DBTestBase):
    def setUp(self):
        super(SellerManagementViewTest,self).setUp()
        self.factory=RequestFactory()
        self.data=''
        self.user=self.the_user
        self.user.setSeller(True)

        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })

        self.sku2 = self.entity.add_sku({
            'color': 'black',
            'size': 128
        })
        self.sku1.stock = 2432
        self.sku2.stock = 2423
        self.user.add_sku_to_cart(self.sku1)
        self.user.add_sku_to_cart(self.sku2)
        self.new_order = self.user.checkout()
    def test_seller_management_view(self):
        request_url = reverse('web_seller_management')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagement.as_view()(request)
        pprint("******")
        pprint('test SellerManagement...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)
    def test_qrcode_list_view(self):
        request_url = reverse('web_seller_management_qrcode_list')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = QrcodeListView.as_view()(request)
        pprint("******")
        pprint('test QrcodeListView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)
    def test_seller_management_order_view(self):
        request_url = reverse('web_seller_management_order_list')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagementOrders.as_view()(request)
        pprint("******")
        pprint('test SellerManagementOrders...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)
    def test_seller_management_sold_entity_list_view(self):
        request_url = reverse('web_seller_management_sold_entity_list')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagementSoldEntityList.as_view()(request)
        pprint("******")
        pprint('test SellerManagementSoldEntityList...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_seller_management_sku_save(self):
        pass

    def test_seller_management_add_entity(self):
        request_url = reverse('web_seller_management_entity_add')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagementAddEntity.as_view()(request)
        pprint("******")
        pprint('test SellerManagementAddEntity...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_seller_management_financial_report(self):
        request_url = reverse('web_seller_management_financial_reports')
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagementFinancialReport.as_view()(request)
        pprint("******")
        pprint('test SellerManagementFinancialReport...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_sku_create_view(self):
        request_url = reverse('sku_add_box',args=[self.entity.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SKUCreateView.as_view()(request)
        pprint("******")
        pprint('test SKUCreateView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_seller_management_entity_save(self):
        request_url = reverse('web_seller_management_entity_save', args=[self.entity.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SellerManagementEntitySave.as_view()(request)
        pprint("******")
        pprint('test SellerManagementEntitySave...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_sku_list_view(self):
        request_url = reverse('sku_list_management', args=[self.entity.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SKUListView.as_view()(request)
        pprint("******")
        pprint('test SKUListView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_sku_status_change_view(self):
        pass
    def test_order_detail_view(self):
        request_url = reverse('order_detail_management', args=[self.new_order.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = OrderDetailView.as_view()(request)
        pprint("******")
        pprint('test OrderDetailView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_sku_delete_view(self):
        request_url = reverse('sku_delete_management', args=[self.new_order.id,self.sku1.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SKUDeleteView.as_view()(request)
        pprint("******")
        pprint('test SKUDeleteView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

    def test_sku_update_management(self):
        request_url = reverse('sku_update_management', args=[self.entity.id,self.sku1.id])
        request = self.factory.get(request_url, self.data)
        request.user = self.user
        response = SKUUpdateView.as_view()(request)
        pprint("******")
        pprint('test SKUUpdateView...')
        pprint(dir(response))
        pprint(response._headers)
        self.assertEqual(response.status_code, 200)

