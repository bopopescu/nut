#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR+'../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

from django.conf import settings
from apps.core.models import GKUser
from sendcloud.address_list import SendCloudAddressList


all_gkusers = GKUser.objects.all()

for user in all_gkusers:
    print '> ', user.nickname
    nickname = user.nickname
    sd_mem = SendCloudAddressList(member_addr=user.email)
    print sd_mem.add_member(name=nickname, upsert='true')
    print ''
