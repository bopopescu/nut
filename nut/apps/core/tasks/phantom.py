#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverFactory(object):

    __instance = None

    @classmethod
    def get(cls):
        if not cls.__instance:
            print('initialize phantom webdriver')
            cls.__instance = webdriver.PhantomJS(
                executable_path='/usr/local/bin/phantomjs',
                service_args='--disk-cache true --load-images false'.split()
            )
        return cls.__instance


# @task(name='get_html_source')
def get_html_source(url, expected_element, timeout=20):
    driver = DriverFactory.get()
    driver.get(url)
    WebDriverWait(
        driver, timeout
    ).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, expected_element))
    )
    html = driver.page_source.encode('utf-8')
    return html
