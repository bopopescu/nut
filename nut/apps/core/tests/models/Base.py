from apps.core.models import Entity, GKUser, Category, Sub_Category, Buy_Link
from django.test import TestCase

from apps.shop.models import Shop


class DBTestBase(TestCase):
    def setUp(self):
        self.the_user = GKUser.objects.create_user(**{
            'username': 'test_user',
            'email': 'anchen_test@guoku.com',
            'is_active':  1,
            'is_admin': False,
            'password': 'test_pass'
        })
        self.category = Category.objects.create(**{
            'title': 'test_category_title',
            'status': True
        })

        self.sub_category = Sub_Category.objects.create(**{
            'group': self.category,
            'title': 'test_sub_category_title',
            'alias': 'test_sub_cate_alias',
            'status': True
        })

        self.entity = Entity.objects.create(**{
            'user': self.the_user,
            'entity_hash': 'test_hash',
            'category': self.sub_category,
            'brand': 'guoku_test_brand',
            'title': 'test_entity_title',
            'images':  ["http://img01.taobaocdn.com/bao/uploaded/i1/T1Rgl7XkBtXXbGKWs._111251.jpg"],
            'status': 0
        })


class Order_Test_Base(DBTestBase):
    def setUp(self):
        super(Order_Test_Base, self).setUp()
        self.sku1 = self.entity.add_sku({
            'color': 'red',
            'size': 165
        })
        self.sku1.stock = 5
        self.sku1.origin_price = 0.02
        self.sku1.promo_price = 0.01
        self.sku1.save()

        self.sku2 = self.entity.add_sku({
            'color': 'black',
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








