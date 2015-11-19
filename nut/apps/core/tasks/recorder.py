#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from datetime import datetime
from django.contrib.auth.models import AnonymousUser

from apps.core.models import Search_History
from apps.core.tasks import BaseTask
from django.utils.log import getLogger

log = getLogger('django')


@task(base=BaseTask, name='record_search')
def _record_search(gk_user, **kwargs):
    if gk_user and isinstance(gk_user, AnonymousUser):
        gk_user = None

    key_words = kwargs.pop('key_words')
    if not key_words:
        return
    footprint = Search_History(user=gk_user,
                               key_words=key_words,
                               search_time=datetime.now())
    footprint.save()


def record_search(gk_user, **kwargs):
    """
    Record search history.
    Args:
        kwargs: search key words.
        gk_user: GKUser object or id of a GKUser.
    """
    result = _record_search.delay(gk_user, **kwargs)
    if result.failed():
        log.warning("Recording was: %s" % result.result)
