# coding=utf-8

from apps.order.tests import DBTestBase
from apps.core.models import SKU,Entity,GKUser, Category, Sub_Category
from apps.order.models import CartItem, ShippingAddress
from apps.order.exceptions import  CartException, OrderException,PaymentException


class OrderForUserTest(DBTestBase):
    #see DBTestBase for pre setuped vars
    def setUp(self):
        super(OrderForUserTest, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size':165
        })
        self.sku1.stock = 5
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color':'black',
            'size': 128
        })
        self.sku2.stock = 5
        self.sku2.save()

        self.normal_address = ShippingAddress(**{
            'type':ShippingAddress.normal,
            'country':'china',
            'province':'beijing',
            'city':'beijing',
            'street':'chang an jie',
            'detail': 'zhong nan hai, zi guang ge',
            'post_code':'100010',
        })

        self.special_address = ShippingAddress(**{
            'type':ShippingAddress.special
        })


    def test_user_checkout_empty_cart_raise_cart_exception(self):
        #create order base on user's cart
        self.assertEqual(self.the_user.cart_item_count, 0)
        with self.assertRaises(CartException):
            self.the_user.checkout()

    def test_user_checkout_create_order(self):
        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.add_sku_to_cart(self.sku2)
        self.assertEqual(self.the_user.cart_item_count, 2)
        self.the_user.checkout()


        pass

    def test_user_checkout_create_order_items(self):
        pass
