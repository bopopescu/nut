# coding=utf-8
from pprint import  pprint

from django.test import TestCase


from django.conf import  settings
from django.core.exceptions import ImproperlyConfigured

from apps.core.models import Entity,GKUser, Category, Sub_Category
from apps.order.models import CartItem , SKU
from apps.order.exceptions import  CartException, OrderException,PaymentException


# checkout if in test env



class CartForUserTest(TestCase):
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


    def test_entity_sku_add_return_sku_instance(self):
        entity  = self.entity
        sku = entity.add_sku({
            'size':188
        })
        self.assertIsInstance(sku, SKU)
        self.assertEqual(sku.attrs, {'size':188})
        self.assertNotEqual(sku.attrs, {'size':199})
        self.assertEqual(entity.skus.all().count(), 1)
        self.assertNotEqual(entity.skus.all().count(),2)

    def test_sku_count(self):
        entity = self.entity
        entity.add_sku()
        entity.add_sku({
            'color':'red'
        })
        self.assertEqual(entity.skus.all().count() , 2)
        entity.add_sku({
            'color':'red'
        })
        self.assertEqual(entity.skus.all().count(), 2)

        entity.add_sku({
            'color':'blue'
        })
        self.assertEqual(entity.skus.all().count(), 3)


    def test_add_zero_stock_sku_to_cart_raise_cart_exception(self):
        user = self.the_user
        sku = self.entity.add_sku()
        with self.assertRaises(CartException):
            user.add_sku_to_cart(sku)
        self.assertEqual(0, user.cart_item_count)


    def test_sku_can_be_added_to_cart(self):
        # sku =  self.entity.add_sku({'size':165})
        # self.user.add_sku_to_cart(sku)
        user = self.the_user
        #at start there is no sku for entity
        self.assertEqual(self.entity.sku_count, 0)


        sku = self.entity.add_sku()
        sku.stock = 5 #make sure the stock is greater than 0
        self.the_user.add_sku_to_cart(sku)
        self.assertEqual(user.cart_item_count , 1)

        #add same sku to user's cart , still , item_count is 1
        self.the_user.add_sku_to_cart(sku)
        self.assertEqual(user.cart_item_count, 1)


        self.assertEqual(self.the_user.cart_items.all()[0].volume, 2)

        self.the_user.add_sku_to_cart(sku)
        self.assertEqual(self.the_user.cart_items.all()[0].volume, 3)

        #add an other sku for entity
        #set stock greater than 0
        sku2 = self.entity.add_sku({
            'color':'green'
        })

        sku2.stock=5
        sku2.save()
        self.the_user.add_sku_to_cart(sku2)

        self.assertEqual(self.the_user.cart_item_count , 2)




















def run_test():
    pass

if __name__ == '__main__':
    run_test()

