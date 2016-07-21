#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import task
from django.contrib.auth.models import AnonymousUser
import requests

# from apps.core.models import Search_History
from apps.core.tasks import BaseTask

from django.conf import settings
from django.utils.log import getLogger
log = getLogger('django')

record_host = getattr(settings, 'RECORD_KEYWORD_SERVER', None)


@task(base=BaseTask, name='record_search')
def _record_search(gk_user, key_words, ip_address, user_agent):
    payload = dict()
    payload.update(
        {
            'key': key_words,
            'ip': ip_address,
            'ua': user_agent,
        }
    )
    if gk_user and isinstance(gk_user, AnonymousUser):
        pass
    else:
        payload.update(
            {
                'uid': gk_user.pk,
            }
        )
    url = "{0}/keywords/".format(record_host)
    # log.error(url)
    r = requests.post(url, data=payload)
    # if not key_words:
    #     return
    # footprint = Search_History(user=gk_user,
    #                            key_words=key_words,
    #                            search_time=datetime.now(),
    #                            ip=ip_address,
    #                            agent=user_agent)
    # footprint.save()
    # log.error(r.text)
    if r.status_code == 201:
        return r.json()
    r.close()

    # else:
    #     return None

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
    # res = _record_search(gk_user, key_words, ip_address, user_agent)
    result = _record_search.delay(gk_user, key_words, ip_address, user_agent)
    if result.failed():
        log.warning("Recording was: %s" % result.result)
