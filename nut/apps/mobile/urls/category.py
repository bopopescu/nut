from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.category',
    url(r'^$', 'list', name='mobile_category_list'),
)

__author__ = 'edison'
