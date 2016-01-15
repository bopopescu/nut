#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from celery.utils.log import get_task_logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger = get_task_logger(__name__)


class DriverFactory(object):
    __instance = None

    @classmethod
    def get(cls):
        if not cls.__instance:
            print('initialize phantom web driver')
            # '--load-stylesheet false '
            cls.__instance = webdriver.PhantomJS(
                executable_path='/usr/local/bin/phantomjs',
                service_args='--disk-cache true '
                             '--load-images false '
                             '--cookies-file phantom.cookies'.split()
            )
        return cls.__instance


@task(name='get_html_source')
def get_html_source(url, expected_element, timeout=20):
    timeout = int(timeout)
    if not url:
        return

    html = ''
    driver = DriverFactory.get()
    driver.get(url)
    print ">> Start to fetching %s" % url
    try:
        if expected_element:
            WebDriverWait(
                driver, timeout
            ).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, expected_element))
            )
        logger.info('[Phantom] Crawled. url:%s' % url)
        html = driver.page_source.encode('utf-8')
    except TimeoutException, e:
        logger.warning('[Phantom] Timeout. url: %s. %s' % (url, e.message))
    except WebDriverException, e:
        logger.error(
            '[Phantom] WebDriverException. url:%s. %s' % (url, e.message))
    return html
