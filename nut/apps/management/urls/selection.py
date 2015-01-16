from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.selection',
    url(r'^$', 'list', name='management_selection_list'),
)

__author__ = 'edison7500'
