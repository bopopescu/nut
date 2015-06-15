from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.tags',
    url(r'^$', 'list', name='management_tag_list'),
    url(r'^(?P<tag_id>\d+)/edit/$', 'edit', name='management_tag_edit'),
)

__author__ = 'edison'
