from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.mobile.views',
    url(r'^homepage/$', 'homepage', name='mobile_homepage')
)


__author__ = 'edison7500'
