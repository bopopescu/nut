from django.conf.urls import url, patterns
from django.views.generic import RedirectView
from apps.management.views.selection import PrepareBatchSelection, \
                                            DoBatchSelection,\
                                            RemoveBatchSelection

urlpatterns = patterns(
    'apps.management.views.selection',

    url(r'^$', RedirectView.as_view(url="/management/selection/published/"), name='management_selection_list'),
    url(r'^published/$', 'published', name='management_selection_published'),
    url(r'^pending/$', 'pending', name='management_selection_pending'),
    url(r'^pending_and_removed/$', 'pending_and_removed', name='management_selection_pending_and_removed'),
    url(r'^publish/(?P<sid>\d+)/edit/$', 'edit_publish', name='management_selection_edit_publish'),

    url(r'^set/publish/datetime/$', 'set_publish_datetime', name='management_set_publish_datetime'),
    url(r'^set/publish/batch/prepare/$', PrepareBatchSelection.as_view(), name='management_batch_selection_prepare'),
    url(r'^set/publish/batch/do/$', DoBatchSelection.as_view(), name='management_batch_selection_do'),
    url(r'^set/remove/batch/do/$', RemoveBatchSelection.as_view(), name='management_batch_selection_remove'),
    url(r'^popular/$', 'popular', name='management_selection_popular'),
    url(r'^usite/publish/$', 'usite_published', name='management_usite_published'),
)

__author__ = 'edison7500'
