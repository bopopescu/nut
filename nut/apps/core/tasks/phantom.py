#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
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
                service_args='--disk-cache true --load-images false --load-stylesheet false'.split()
            )
        return cls.__instance


@task(name='get_html_source')
def get_html_source(url, expected_element, timeout=20):
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n%s\r\n-----011000010111000001101001--"%url
    headers = {
        'content-type': "multipart/form-data; boundary=---011000010111000001101001",
        'cache-control': "no-cache",
        'postman-token': "03f1b0da-9ac1-7595-6e99-7c17ba4fca15"
    }
    phantom_server = "http://10.0.2.49:5000/"
    response = requests.request("POST", phantom_server, data=payload, headers=headers)
    html = response.content
    return html
