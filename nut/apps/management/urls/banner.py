from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.banner',
    url(r'^$', 'list', name='management_banner_list'),
    url(r'^add/$', 'create', name='management_banner_create'),
)


__author__ = 'edison'
