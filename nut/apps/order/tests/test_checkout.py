from pprint import pprint

from apps.order.tests import  DBTestBase
from apps.core.models import GKUser
from apps.order.exceptions import OrderException, CartException
from apps.order.models import Order, SKU


class Checkout_Test(DBTestBase):
    def setUp(self):
        super(Checkout_Test, self).setUp()

        self.the_user_2 = GKUser.objects.create_user(**{
            'username': 'test_user_2',
            'email': 'anchen_test_2@guoku.com',
            'is_active':  1,
            'is_admin': False,
            'password': 'test_pass'
        })

        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })

        self.sku1.stock = 5
        self.sku1.origin_price = 0.02
        self.sku1.promo_price = 0.01
        self.sku1.save()

    def test_checkout_reduce_sku_stock(self):
        self.the_user.add_sku_to_cart(self.sku1, 3)
        self.the_user.checkout()
        self.sku1 = SKU.objects.get(id=self.sku1.id)
        self.assertEqual(self.sku1.stock, 2)


    def test_checkout_sku_out_of_stock(self):

        # add sku to cart is ok , even total cart item count greater than sku stock
        self.the_user.add_sku_to_cart(self.sku1, 3)
        self.the_user_2.add_sku_to_cart(self.sku1, 3)

        #simulate a sku stock reduce event , like order checkout  or ....
        self.sku1.stock = 2
        self.sku1.save()

        #now , user can not checkout there cart

        # and throw order

        with self.assertRaises(CartException) as context:
            self.the_user.checkout()
            self.assertTrue('some cart item is out of stock' in context.exception)

        with self.assertRaises(CartException) as context:
            self.the_user_2.checkout()
            self.assertTrue('some cart item is out of stock' in context.exception)


        self.sku1.stock = 5
        self.sku1.save()
        #now  first user can checkout , second user will raise CartException

        order = self.the_user.checkout()
        self.assertIsInstance(order, Order)
        self.assertEqual(order.items.all().count(), 1)
        self.assertEqual(order.items.all()[0].volume, 3)

        with self.assertRaises(CartException) as context:
            self.the_user_2.checkout()
            pprint(context)


