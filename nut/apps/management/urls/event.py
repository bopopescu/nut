from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.management.views.event',
    url(r'^$', 'list', name='management_event'),
    url(r'^create/$', 'create', name='management_event_create'),
    url(r'^edit/(?P<eid>\d+)/$', 'edit', name='management_event_edit'),

    #for article related management url


)

__author__ = 'edison7500'
