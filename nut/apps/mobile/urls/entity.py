from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.entity',
    url(r'^$', 'list', name='mobile_entity_list'),
)


__author__ = 'edison'
