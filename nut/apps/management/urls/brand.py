from django.conf.urls import url, patterns

from apps.management.views.brand import \
    BrandListView, BrandEntityListView, \
    BrandStatView, BrandEditView, \
    BrandCreateView, BrandNameEditView,\
    AddBrandEntityView, BrandSelectedEntitiesView

urlpatterns = patterns(
    'apps.management.views.brand',
    url(r'^$', BrandListView.as_view(), name='management_brand_list'),
    url(r'^stat/$', BrandStatView.as_view(), name='management_brand_stat'),
    url(r'^create/$', BrandCreateView.as_view(), name='management_brand_create'),

    url(r'^(?P<brand_id>\d+)/edit/$', BrandEditView.as_view(), name='management_brand_edit'),
    url(r'^(?P<brand_name>.+)/edit/$', BrandNameEditView.as_view(), name='management_brand_name_edit'),
    url(r'^(?P<brand_id>\d+)/name/(?P<brand>.+)/$', BrandEntityListView.as_view(), name='management_brand_entity_list'),
    url(r'^add/entity/$', AddBrandEntityView.as_view(), name='management_brand_add_entity'),
    url(r'^(?P<brand_id>\d+)/selected_entity/$', BrandSelectedEntitiesView.as_view(), name='management_brand_selected_entity_json'),


    # url(r'^add/$', 'create', name='management_banner_create'),
    # url(r'^(?P<banner_id>\d+)/edit/$', 'edit', name='management_banner_edit'),


)

__author__ = 'edison'
