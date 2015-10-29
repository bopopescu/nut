#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.management.views.edm import EDMListView, EDMUpdate
from apps.management.views.edm import EDMCreate


urlpatterns = patterns(
    'apps.management.views.edm',
    url(r'^$', EDMListView.as_view(), name='management_edm_list'),
    url(r'^edit/(?P<pk>\d+)/$', EDMUpdate.as_view(), name='management_edm_edit'),
    url(r'^create/$', EDMCreate.as_view(), name='management_edm_create'),
    url(r'^preview/(?P<edm_id>\d+)/$', 'preview_edm', name='preview_edm'),
    url(r'^send/(?P<edm_id>\d+)/$', 'send_edm', name='send_edm'),
    url(r'^approval/(?P<edm_id>\d+)/$', 'approval_edm', name='approval_edm'),
    url(r'^sync/(?P<edm_id>\d+)/$', 'sync_verify_status', name='sync_verify_status'),
    url(r'^delete/(?P<edm_id>\d+)/$', 'edm_delete', name='delete_edm'),
)
print urlpatterns
