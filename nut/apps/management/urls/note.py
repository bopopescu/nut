from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.note',
    url(r'^$', 'list', name='management_note_list'),
    # url(r'^(?P<entity_id>\d+)/edit/$', 'edit', name='management_entity_edit'),
)

__author__ = 'edison'
