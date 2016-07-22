# coding=utf-8

from apps.order.tests import DBTestBase
from apps.core.models import SKU,Entity,GKUser, Category, Sub_Category
from apps.order.models import CartItem, ShippingAddress, Order, OrderItem
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
        self.sku1.origin_price = 7
        self.sku1.promo_price = 5
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color':'black',
            'size': 128
        })
        self.sku2.stock = 5
        self.sku2.origin_price = 13
        self.sku2.promo_price = 11
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

    def test_add_sku_to_cart_price_cal(self):
        cart_item = self.the_user.add_sku_to_cart(self.sku1)
        self.assertEqual(cart_item.volume , 1)
        self.assertEqual(cart_item.grand_total_price, 7)

        #add same sku twice
        cart_item = self.the_user.add_sku_to_cart(self.sku1)
        self.assertEqual(cart_item.volume, 2)
        self.assertEqual(cart_item.grand_total_price, 14)


    def test_user_checkout_create_order(self):
        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.add_sku_to_cart(self.sku2)
        self.the_user.add_sku_to_cart(self.sku2)

        self.assertEqual(self.the_user.cart_item_count, 2)

        new_order  = self.the_user.checkout()

        # new_order is a instance of  Order
        self.assertIsInstance(new_order,Order)

        # order item is 2
        self.assertEqual(new_order.items.count(), 2)

        #user got 1 order
        self.assertEqual(self.the_user.order_count, 1)

        #cart is cleared
        self.assertEqual(self.the_user.cart_item_count , 0)

        #
        self.assertEqual(self.the_user.order_items.all()[1].volume , 2)



    def test_user_checkout_order_price(self):
        self.the_user.add_sku_to_cart(self.sku1)
        self.the_user.add_sku_to_cart(self.sku2)
        self.the_user.checkout()

        the_order = self.the_user.orders.all()[0]

        self.assertIsInstance(the_order, Order)

        self.assertEqual(the_order.items.count(), 2)
        self.assertEqual(the_order.items.all()[0].volume , 1)
        self.assertEqual(the_order.items.all()[1].volume , 1)

        order_items = the_order.items.all()
        print [item.grand_total_price for item in order_items]
        total_price = reduce(lambda a, b : a+b, [item.grand_total_price for item in order_items])
        self.assertEqual(total_price, 20)


        self.assertEqual(the_order.grand_total_price, 20)
        self.assertEqual(the_order.promo_total_price, 16)

    def test_add_sku_more_volume_than_stock_raise_exception(self):
        with self.assertRaises(CartException):
            self.sku1.stock = 3
            self.the_user.add_sku_to_cart(sku=self.sku1, volume=4)


    def test_user_checkout_order_more_sku_volume(self):
        self.sku1.stock = 6
        self.sku2.stock = 13
        self.the_user.add_sku_to_cart(self.sku1, 5)
        self.the_user.add_sku_to_cart(self.sku2, 12)
        order = self.the_user.checkout()
        self.assertEqual(order.grand_total_price, 7*5 +13*12)
        self.assertEqual(order.promo_total_price, 5*5 + 11*12)







