from django.conf.urls import patterns, include, url
from django.conf import settings
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'management/', include('apps.management.urls')),
    # url(r'^', include('apps.web.urls')),

    url(r'^api/', include('apps.api.urls')),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )