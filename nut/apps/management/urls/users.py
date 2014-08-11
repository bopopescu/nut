from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.users',
    url(r'^$', 'list', name='management_user_list'),
)

__author__ = 'edison'
