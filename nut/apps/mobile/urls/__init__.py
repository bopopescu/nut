from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.mobile.views',
    url(r'^homepage/$', 'homepage', name='mobile_homepage'),
)

urlpatterns += patterns(
    'apps.mobile.views.entity',
    url(r'^entity/', include('apps.mobile.urls.entity')),
)


__author__ = 'edison7500'
