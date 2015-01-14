from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.entity',
    url(r'^$', 'list', name='mobile_entity_list'),
    url(r'^(?P<entity_id>\d+)/$', 'detail', name='mobile_entity_detail'),
)


__author__ = 'edison'
