from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.management',
    url(r'^$', 'views.dashboard', name='management_dashboard'),
    url(r'^entity/', include('apps.management.urls.entities')),

)

__author__ = 'edison7500'
