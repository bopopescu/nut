from django.conf.urls import url, patterns
# from apps.management.views.entities import EntityListView

urlpatterns = patterns(
    'apps.management.views.entities',
    # url(r'^$', EntityListView.as_view(), name='management_entity_list'),
    url(r'^$', 'list', name='management_entity_list'),
    url(r'^(?P<entity_id>\d+)/edit/$', 'edit', name='management_entity_edit'),
)

__author__ = 'edison7500'
