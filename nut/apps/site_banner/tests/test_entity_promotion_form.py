from apps.site_banner.forms import entity_url_re , EntityPromotionForm
from unittest import TestCase
class TestEntityPromotionForm(TestCase):
    def test_url_clean(self):
        url = 'http://www.guoku.com/detail/3286db84/'

