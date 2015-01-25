from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.event_banner',
    url(r'^$', 'list', name='management_event_banner'),
    url(r'^(?P<sid>\d+)/$', 'show_list', name='management_event_show_banner'),
    url(r'^create/$', 'create', name='management_event_banner_create'),
    url(r'^create/(?P<event_id>\d+)/$', 'create', name='management_event_banner_create'),
    url(r'^(?P<event_banner_id>\d+)/edit/$', 'edit', name='management_event_banner_edit'),
)

__author__ = 'edison'
