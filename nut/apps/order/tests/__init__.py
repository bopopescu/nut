from apps.core.models import Entity,GKUser, Category, Sub_Category
from apps.order.models import SKU
from django.test import  TestCase

class DBTestBase(TestCase):
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