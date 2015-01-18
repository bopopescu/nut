from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.mobile.views',
    url(r'^homepage/$', 'homepage', name='mobile_homepage'),
    url(r'^selection/$', 'selection', name='mobile_selection'),
    url(r'^popular/$', 'popular', name='mobile_popular'),
    url(r'^item/(?P<item_id>\d+)/$', 'visit_item', name='mobile_visit_item'),
)

urlpatterns += patterns(
    'apps.mobile.views.account',
    url(r'^login/$', 'login', name='mobile_login'),
    url(r'^logout/$', 'logout', name='mobile_logout')
)

urlpatterns += patterns(
    'apps.mobile.views.entity',
    url(r'^entity/', include('apps.mobile.urls.entity')),
    url(r'^category/', include('apps.mobile.urls.category')),
    url(r'^user/', include('apps.mobile.urls.user')),
)


__author__ = 'edison7500'
