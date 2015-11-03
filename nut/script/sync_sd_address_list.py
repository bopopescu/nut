#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from apps.core.models import GKUser


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR+'../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

sd_list = 'all_gkusers@maillist.sendcloud.org'

all_gkusers = GKUser.objects.all()

for user in all_gkusers:
    pass
