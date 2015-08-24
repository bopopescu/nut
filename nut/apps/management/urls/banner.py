from django.conf.urls import url, patterns
from apps.management.views.banner import BannerListView


urlpatterns = patterns(
    'apps.management.views.banner',
    url(r'^$', BannerListView.as_view(), name='management_banner_list'),
    url(r'^add/$', 'create', name='management_banner_create'),
    url(r'^(?P<banner_id>\d+)/edit/$', 'edit', name='management_banner_edit'),
)


__author__ = 'edison'
