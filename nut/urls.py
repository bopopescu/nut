from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = staticfiles_urlpatterns()
# from django.contrib import admin
# admin.autodiscover()


handler500 = 'apps.web.views.page_error'
handler404 = 'apps.web.views.webpage_not_found'
handler403 = 'django.views.defaults.permission_denied'


urlpatterns += patterns(
    '',
    url(r'^403/$', 'django.views.defaults.permission_denied'),
    url(r'^404/$', 'apps.web.views.webpage_not_found'),
    url(r'^500/$', 'apps.web.views.page_error'),
    # (r'^visit_item/$', 'mobile.views.old_visit_item'),
)

urlpatterns += patterns('',

    url(r'^management/', include('apps.management.urls')),
    url(r'^mobile/v3/', include('apps.mobile.urls')),
    url(r'^api/', include('apps.api.urls')),

    # url(r'^$', 'apps.web.views.main.index', name='web_index'),
    # url(r'^', include('apps.web.urls')),
    # url(r'^selection/')
    url(r'^', include('apps.web.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )