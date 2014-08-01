from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.entities',

    url(r'^$', 'list', name='management_entity_list'),
)

__author__ = 'edison7500'
