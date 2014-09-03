from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.category',
    url(r'^(?P<category_id>\d+)/$', 'list', name='management_category_list'),
    url(r'^$', 'list', name='management_category_list'),

)

__author__ = 'edison'
