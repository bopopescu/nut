from django.test import TestCase


class AccountTemplateTest(TestCase):
    def test_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, template_name='web/account/login.html')
