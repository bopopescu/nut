from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.category',
    url(r'^$', 'list', name='mobile_category_list'),
    url(r'^(?P<category_id>\d+)/stat/$', 'stat', name='mobile_category_stat'),
    url(r'^(?P<category_id>\d+)/entity/$', 'entity', name='mobile_category_entity'),
)

__author__ = 'edison'
