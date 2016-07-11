# coding=utf-8
from django.test import TestCase


from django.conf import  settings
from django.core.exceptions import ImproperlyConfigured

from apps.core.models import SKU,Entity,GKUser, Category, Sub_Category
from apps.order.models import CartItem



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



    def test_sku_can_be_added_to_cart(self):


        pass






def run_test():
    pass


if __name__ == '__main__':
    run_test()

