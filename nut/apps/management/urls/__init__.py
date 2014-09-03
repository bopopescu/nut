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
    url(r'^comment/', include('apps.management.urls.comments')),
    url(r'^category/', include('apps.management.urls.category')),
    url(r'^t/', include('apps.management.urls.tags')),
)

__author__ = 'edison7500'
