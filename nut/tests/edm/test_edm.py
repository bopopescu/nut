#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from apps.core.tasks import send_forget_password_mail


def test_send_forget_password_mail(client, gk_user):
    send_forget_password_mail(gk_user)
