from django.test import TestCase


class AccountTemplateTest(TestCase):

    def test_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, template_name='web/account/login.html')


# class AccountFunCTest(TestCase):

    # def test_user_login(self):
    #     response    = self.client.get('/login/')
    #     self.assertEqual(response.status_code, 200)

        # response    = self.client.post('/login/', {
        #     'email'     : 'jiaxin@guoku.com',
        #     'password'  : 'jessie1@#'
        # })
        #
        # self.assertEqual(response.status_code, 302)
        #
        # self.assertEqual(response['location'], '/')