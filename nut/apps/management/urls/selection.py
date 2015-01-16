from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.selection',

    url(r'^$', 'selection_list', name='management_selection_list'),
    url(r'^published/$', 'published', name='management_selection_published'),
    url(r'^pending/$', 'pending', name='management_selection_pending'),
    url(r'^publish/(?P<sid>\d+)/edit/$', 'edit_publish', name='management_selection_edit_publish'),

    url(r'set/publish/datetime/$', 'set_publish_datetime', name='management_set_publish_datetime'),
)

__author__ = 'edison7500'
