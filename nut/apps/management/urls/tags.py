from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.tags',
    url(r'^$', 'list', name='management_tag_list'),
)

__author__ = 'edison'
