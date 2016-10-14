from django.core.urlresolvers import resolve
from django.test import TestCase
from apps.v4.views import HomeView


class HomeViewTest(TestCase):

    def test_home_url(self):
        found = resolve('/mobile/v4/home/')
        self.assertEqual(found.func, HomeView)


if __name__ == "__main__":
    t = HomeViewTest()
    t.test_home_url()