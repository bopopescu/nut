from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.category',
    url(r'^$', 'list', name='mobile_category_list'),
    url(r'^(?P<category_id>\d+)/stat/', 'category_stat', name='mobile_category_stat'),
)

__author__ = 'edison'
