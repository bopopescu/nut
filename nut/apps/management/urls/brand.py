from django.conf.urls import url, patterns

from apps.management.views.brand import BrandListView, BrandEntityListView, BrandStatView

urlpatterns = patterns(
    'apps.management.views.brand',
    url(r'^$', BrandListView.as_view(), name='management_brand_list'),
    url(r'^stat/$', BrandStatView.as_view(), name='management_brand_stat'),
    url(r'^(?P<brand>.+)/$', BrandEntityListView.as_view(), name='management_brand_entity_list'),
    # url(r'^add/$', 'create', name='management_banner_create'),
    # url(r'^(?P<banner_id>\d+)/edit/$', 'edit', name='management_banner_edit'),
)

__author__ = 'edison'
