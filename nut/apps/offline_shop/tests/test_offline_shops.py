from apps.order.tests import DBTestBase
from apps.offline_shop.models import Offline_Shop_Info
from apps.core.models import GKUser

class OfflineShopTest(DBTestBase):
    def setUp(self):
        super(OfflineShopTest, self).setUp()
        self.the_user.setOfflineShop(True)
        self.shop = Offline_Shop_Info.objects.create(shop_owner_id=self.the_user.id)
        self.shop.status = True
        self.shop.save()

    def test_Offline_Shop_Info_Manager(self):
        active_shops = Offline_Shop_Info.objects.active_offline_shops()
        self.assertEqual(len(active_shops), 1)
        self.assertEqual(self.the_user.is_offline_shop, True)


    def test_multi_offline_shop(self):
        #create new offline shop
        self.new_user = GKUser.objects.create_user(**{
            'username': 'test_user_2',
            'email': 'anchen_test_2@guoku.com',
            'is_active':  1,
            'is_admin': False,
            'password': 'test_pass'
        })

        self.new_user.setOfflineShop(True)
        new_shop = Offline_Shop_Info.objects.create(shop_owner_id=self.new_user.id)

        active_shops = Offline_Shop_Info.objects.active_offline_shops()

        #new shop is inactive by default
        self.assertEqual(len(active_shops), 1)

        new_shop.status = True
        new_shop.save()
        active_shops = Offline_Shop_Info.objects.active_offline_shops()

        self.assertEqual(len(active_shops), 2)

    def test_mobile_url(self):
        shop = self.shop
        print(shop.mobile_url)

        self.assertIsInstance(shop.mobile_url, basestring)
        self.assertTrue('m.guoku.com' in shop.mobile_url)





