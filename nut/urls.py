from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'management/', include('apps.management.urls')),
    # url(r'^', include('apps.web.urls')),
)
