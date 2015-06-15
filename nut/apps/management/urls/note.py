from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.note',
    url(r'^$', 'list', name='management_note_list'),
    url(r'^(?P<note_id>\d+)/edit/$', 'edit', name='management_note_edit'),
    url(r'^create/(?P<entity_id>\d+)/$', 'create', name='management_note_create'),
)

urlpatterns += patterns(
    'apps.management.views.note_comment',
    url(r'^comment/(?P<note_id>\d+)/$', 'note_comment_list', name='management_note_comment_list'),
)


__author__ = 'edison'
