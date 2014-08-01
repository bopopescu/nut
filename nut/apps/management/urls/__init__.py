from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.management',

    url(r'^entity/', include('apps.management.urls.entities')),
    url(r'^', 'views.dashboard', name='management_dashboard'),
)

__author__ = 'edison7500'
