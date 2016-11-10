# coding=utf-8

from apps.order.tests import DBTestBase
from apps.order.exceptions import CartException


class  SKUCouponTest(DBTestBase):
    def setUp(self):
        super(SKUCouponTest, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })
        self.sku1.stock = 50
        self.sku1.origin_price = 7
        self.sku1.promo_price = -10
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color': 'black',
            'size': 128
        })
        self.sku2.stock = 500
        self.sku2.origin_price = 13
        self.sku2.promo_price = 100
        self.sku2.save()

        self.sku3 = self.entity.add_sku({
            'color': 'red',
            'size': 128
        })
        self.sku3.stock = 500
        self.sku3.origin_price = 13
        self.sku3.promo_price = 10
        self.sku3.save()


    def test_coupon_sku_is_coupon_property(self):
        self.assertEqual(self.sku1.is_coupon, True)
        self.assertEqual(self.sku2.is_coupon, False)


    def test_cart_total_cart_promo_price(self):
        self.the_user.add_sku_to_cart(self.sku2)

        self.assertEqual(self.the_user.total_cart_promo_price(), 100)

        self.the_user.add_sku_to_cart(self.sku2, 2)

        self.assertEqual(self.the_user.total_cart_promo_price(), 300)

        self.the_user.add_sku_to_cart(self.sku3, 5)
        self.assertEqual(self.the_user.total_cart_promo_price(), 350)


    def test_cart_sku_volum_get(self):
        self.the_user.add_sku_to_cart(self.sku2)
        sku2_count = self.the_user.cart_items.sku_volume(self.the_user, self.sku2)
        self.assertEqual(sku2_count, 1)




    def test_cart_coupon_sku_add_fail_when_not_enough_value(self):
        # add a sku with price 10 to cart
        # this is not enough for coupon use
        # add coupon should raise excepion
        self.the_user.add_sku_to_cart(self.sku3)
        with self.assertRaises(CartException):
            self.the_user.add_sku_to_cart(self.sku1)

    def test_cart_coupon_sku_add_success_when_enouph_value(self):
        self.the_user.add_sku_to_cart(self.sku2)
        self.the_user.add_sku_to_cart(self.sku1)
        self.assertEqual(self.the_user.cart_items.sku_volume(self.the_user, self.sku1), 1)

    def test_cart_coupon_sku_add_fail_when_add_toomuch(self):
        self.the_user.add_sku_to_cart(self.sku2, 4)
        self.the_user.add_sku_to_cart(self.sku3, 22)

        self.the_user.add_sku_to_cart(self.sku1, 4)
        self.the_user.add_sku_to_cart(self.sku1, 2)
        with self.assertRaises(CartException):
            self.the_user.add_sku_to_cart(self.sku1, 1)

    def test_order_total_value_is_caculated_right(self):
        self.the_user.add_sku_to_cart(self.sku2, 2)
        self.the_user.add_sku_to_cart(self.sku1)
        order = self.the_user.checkout()
        self.assertEqual(order.order_total_value, 190)

    def test_order_total_value_is_caculated_right_again(self):
        self.the_user.add_sku_to_cart(self.sku2, 2)
        self.the_user.add_sku_to_cart(self.sku1, 2)
        order = self.the_user.checkout()
        self.assertEqual(order.order_total_value, 180)

    def test_order_checkout_for_illegal_coupon_usage(self):
        self.the_user.add_sku_to_cart(self.sku2,3)
        self.the_user.add_sku_to_cart(self.sku1,3)
        self.the_user.decr_sku_in_cart(self.sku2)
        self.assertEqual(self.the_user.cart_items.sku_volume(self.the_user, self.sku2), 2)
        coupon_check = self.the_user.cart_items.cart_coupon_rule_checked(self.the_user)
        self.assertEqual(coupon_check, False)
        with self.assertRaises(CartException):
            order = self.the_user.checkout()

        self.the_user.add_sku_to_cart(self.sku2)
        order = self.the_user.checkout()
        self.assertEqual(order.order_total_value, 270)






