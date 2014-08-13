from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.banner',
    url('^$', 'list', name='management_banner_list'),
)


__author__ = 'edison'
