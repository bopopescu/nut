# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from celery import Task


class Retry(Exception):
    def __init__(self, countdown=5):
        self.countdown = countdown
        self.message = 'Fetch error, need to login or get new token.'


class RequestsTask(Task):
    abstract = True
    compression = 'gzip'
    default_retry_delay = 5
    send_error_emails = True
    max_retries = 3

    def __call__(self, *args, **kwargs):
        try:
            super(RequestsTask, self).__call__(*args, **kwargs)
        except (requests.Timeout, requests.ConnectionError) as e:
            raise self.retry(exc=e)
        except Retry as e:
            raise self.retry(countdown=e.countdown)
