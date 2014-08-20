from django.conf.urls import url, patterns, include
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    'apps.management',
    url(r'^$', RedirectView.as_view(url = '/management/dashboard/')),
    url(r'^dashboard/$', 'views.dashboard', name='management_dashboard'),
    url(r'^entity/', include('apps.management.urls.entities')),
    url(r'^user/', include('apps.management.urls.users')),
    url(r'^banner/', include('apps.management.urls.banner')),
    url(r'^note/', include('apps.management.urls.note')),
)

__author__ = 'edison7500'
