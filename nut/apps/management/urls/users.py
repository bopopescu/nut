from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.users',
    url(r'^$', 'list', name='management_user_list'),
    url(r'^(?P<user_id>\d+)/edit/$', 'edit', name='management_user_edit'),
)

__author__ = 'edison'
