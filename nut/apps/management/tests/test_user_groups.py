from apps.management.tests import UserTestBaseCase


class TestUserCanBeSetToOfflineShop(UserTestBaseCase):

    def testSetOfflineShop(self):
        self.the_user.setOfflineShop(True)
        self.assertEqual(self.the_user.is_offline_shop, True)

        self.the_user.setOfflineShop(False)
        self.assertEqual(self.the_user.is_offline_shop, False)
