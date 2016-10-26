#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser    = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get('http://www.guoku.com/login/')

        self.assertIn('登录', self.browser.title)
        # header_text     = self.browser.find_element_by_tag_name('h1').text
        # self.assertIn('To-Do', header_text)

        # inputbox        = self.browser.find_element_by_id('id_email')
        # self.assertEqual(
        #     inputbox.get_attribute('placeholder'),
        #     '邮箱'
        # )

        # inputbox.send_keys('Buy peacock feathers')
        # inputbox.send_keys(Keys.ENTER)
        #
        # table   = self.browser.find_element_by_id('id_list_table')
        # rows     = table.browser.find_element_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows)
        # )
        #
        # self.fail('Finish the test !')

if __name__ == '__main__':
    unittest.main()
