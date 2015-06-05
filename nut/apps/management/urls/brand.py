from django.conf.urls import url, patterns

from apps.management.views.brand import BrandListView

urlpatterns = patterns(
    'apps.management.views.brand',
    url(r'^$', BrandListView.as_view(), name='management_brand_list'),
    # url(r'^add/$', 'create', name='management_banner_create'),
    # url(r'^(?P<banner_id>\d+)/edit/$', 'edit', name='management_banner_edit'),
)

__author__ = 'edison'
