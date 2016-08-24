# coding=utf-8
from pprint import  pprint

from django.test import TestCase


from django.conf import  settings
from django.core.exceptions import ImproperlyConfigured

from apps.core.models import Entity,GKUser, Category, Sub_Category
from apps.order.models import CartItem,SKU
from apps.order.exceptions import  CartException, OrderException,PaymentException


# checkout if in test env



class CartForUserOperationTest(TestCase):
    def setUp(self):

        self.the_user = GKUser.objects.create_user(**{
            'username':'test_user',
            'email': 'anchen_test@guoku.com',
            'is_active':  1,
            'is_admin': False,
            'password':'test_pass'
        })

        self.category = Category.objects.create(**{
            'title': 'test_category_title',
            'status': True
        })

        self.sub_category = Sub_Category.objects.create(**{
            'group' : self.category,
            'title': 'test_sub_category_title',
            'alias': 'test_sub_cate_alias',
            'status': True
        })
        self.entity = Entity.objects.create(**{
            'user': self.the_user,
            'entity_hash': 'test_hash',
            'category' : self.sub_category,
            'brand': 'guoku_test_brand',
            'title': 'test_entity_title',
            'images':  ["http://img01.taobaocdn.com/bao/uploaded/i1/T1Rgl7XkBtXXbGKWs._111251.jpg",],
            'status': 0
        })

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

    def test_sku_discount_rate(self):
        self.sku3 =  self.entity.add_sku(attributes={})
        self.sku3.origin_price = 10
        self.sku3.promo_price = 8
        self.sku3.save()
        self.assertEqual(self.sku3.discount, 0.8)

        self.sku4 =  self.entity.add_sku(attributes={})
        self.sku4.origin_price = 0
        self.sku4.promo_price = 3
        self.sku4.save()
        self.assertEqual(self.sku4.discount, 1)

        self.sku5 =  self.entity.add_sku(attributes={})
        self.sku5.origin_price = 1
        self.sku5.promo_price = 0
        self.sku5.save()
        self.assertEqual(self.sku4.discount, 1)


    def test_decr_sku_volum_in_user_cart(self):
        self.the_user.add_sku_to_cart(self.sku1, 3)

        self.the_user.decr_sku_in_cart(self.sku1)
        self.assertEqual(self.the_user.cart_items.all()[0].volume, 2)

        self.the_user.add_sku_to_cart(self.sku1, 2)
        self.assertEqual(self.the_user.cart_items.all()[0].volume, 4)

        self.the_user.decr_sku_in_cart(self.sku1)
        self.assertEqual(self.the_user.cart_items.all()[0].volume, 3)

        self.the_user.decr_sku_in_cart(self.sku1)
        self.the_user.decr_sku_in_cart(self.sku1)
        self.assertEqual(self.the_user.cart_items.all()[0].volume, 1)
        self.assertEqual(self.the_user.cart_item_count, 1)


        self.the_user.decr_sku_in_cart(self.sku1)
        self.assertEqual(self.the_user.cart_item_count, 0)






def run_test():
    pass


if __name__ == '__main__':
    run_test()

