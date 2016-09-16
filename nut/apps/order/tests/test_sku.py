from django.db.models import ProtectedError

from apps.order.tests.test_order import OrderTestBase


class SKU_DELETE_TEST(OrderTestBase):

    def setUp(self):
        super(SKU_DELETE_TEST, self).setUp()

    def test_sku_delete_fail_for_orderitem_protect(self):
        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.checkout()
        with self.assertRaises(ProtectedError):
            self.sku1.delete()

    def test_sku_delete_cascade_to_cartitem(self):
        self.the_user.add_sku_to_cart(self.sku1)
        self.assertEqual(self.the_user.cart_item_count, 1)
        self.sku1.delete()
        self.assertEqual(self.the_user.cart_item_count, 0)
