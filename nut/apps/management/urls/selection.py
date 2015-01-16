from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.selection',
    url(r'^$', 'selection_list', name='management_selection_list'),
    url(r'^edit/publish/$', 'edit_publish', name='management_edit_publish'),
)

__author__ = 'edison7500'
