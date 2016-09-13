from apps.core.tests.models.Base import DBTestBase

from apps.core.models import Entity, GKUser, Buy_Link
from apps.shop.models import Shop


class Seller_Manage_Test_Base(DBTestBase):
    '''
        :param none:

    '''
    def setUp(self):
        super(Seller_Manage_Test_Base, self).setUp()
        self.the_user.setSeller()
        self.seller = self.the_user

        self.common_user = GKUser.objects.create_user(**{
            'username': 'test_user_other',
            'email': 'anchen_test_other@guoku.com',
            'is_active':  1,
            'is_admin': False,
            'password': 'test_pass'
        })

        # shop is belongs to seller
        # the common_shop_link will bridge shop , seller , buy_link , and entity

        self.shop = Shop.objects.create(**{
            'owner': self.seller,
            'shop_title': 'test_shop_title',
            'shop_link': 'https://tldchina.taobao.com/',
            'shop_style': Shop.dress,
            'shop_type': Shop.taobao,
            'common_shop_link': 'http://shop62876401.taobao.com'

        })

        self.entity_added = Entity.objects.create(**{
            'user': self.seller,
            'entity_hash': 'test_hash_01',
            'category': self.sub_category,
            'brand': 'guoku_test_brand',
            'title': 'test_entity_title',
            'images':  ["http://img01.taobaocdn.com/bao/uploaded/i1/T1Rgl7XkBtXXbGKWs._111251.jpg"],
            'status': 0
        })
        # the entity is added by seller ,
        # but the shop_link in core_buy_link table is not belong to seller's shop
        # the shop_link is changed .
        # this entity will show up in User's <seller_entities> property

        self.buy_link_for_added_entity = Buy_Link.objects.create(**{
            'entity': self.entity_added,
            'origin_id': 536387449034,
            'origin_source': 'taobao.com',
            'cid': '30',
            'link': 'http://item.taobao.com/item.htm?id=536387449034',
            'price': 239,
            'volume': 0,
            'rank': 0,
            'default': 1,
            'status': 2,
            # 'shop_link': 'http://shop62876401.taobao.com'
            'shop_link': 'http://shop62876402.taobao.com'
        })

        # this entity is added buy an other user (not the seller)
        # but it will be showed in seller's <seller_entities> property
        # because it belong's seller's shop
        # see the

        self.shop_entity = Entity.objects.create(**{
            'user': self.common_user,
            'entity_hash': 'test_hash_2',
            'category': self.sub_category,
            'brand': 'guoku_test_brand_other',
            'title': 'test_entity_title_other',
            'images':  ["http://img01.taobaocdn.com/bao/uploaded/i1/T1Rgl7XkBtXXbGKWs._111251.jpg"],
            'status': 0
        })

        self.buy_link_for_shop_entity = Buy_Link.objects.create(**{
            'entity': self.shop_entity,
            'origin_id': 536387449032323,
            'origin_source': 'taobao.com',
            'cid': '30',
            'link': 'http://item.taobao.com/item.htm?id=53638744903234',
            'price': 239,
            'volume': 0,
            'rank': 0,
            'default': 1,
            'status': 2,
            'shop_link': 'http://shop62876401.taobao.com'
        })


class Seller_Entities_Test(Seller_Manage_Test_Base):

    def test_seller_entities_property(self):
        self.assertEqual(self.seller.seller_entities.count(), 3)
        self.assertIn(self.shop_entity, self.seller.seller_entities)
        self.assertIn(self.entity_added, self.seller.seller_entities)

