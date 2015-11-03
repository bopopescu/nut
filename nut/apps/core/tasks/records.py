#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from datetime import datetime
from apps.core.tasks import BaseTask
from apps.core.models import Search_History

from django.utils.log import getLogger

log = getLogger('django')


@task(base=BaseTask)
def log_searches(user, key_word):
    footprint = Search_History(
        user=user,
        key_word=key_word,
        search_time=datetime.now()
    )
    footprint.save()
