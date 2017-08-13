#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery.task import task
from apps.core.tasks import BaseTask

from django.conf import settings
from django.utils.log import getLogger

log = getLogger('django')

record_host = getattr(settings, 'RECORD_KEYWORD_SERVER', None)


@task(base=BaseTask, name='record_search')
def _record_search(gk_user, key_words, ip_address, user_agent):
    # TODO: 部署记录服务，重新打开此部分
    return


def record_search(gk_user, **kwargs):
    """
    Record search history.
    Args:
        kwargs: search key words.
        gk_user: GKUser object or id of a GKUser.
    """
    key_words = kwargs.pop('key_words')
    if not key_words:
        return

    ip_address = kwargs.pop('ip_address', None)
    user_agent = kwargs.pop('user_agent', None)
    result = _record_search.delay(gk_user, key_words, ip_address, user_agent)
    if result.failed():
        log.warning("Recording was: %s" % result.result)
