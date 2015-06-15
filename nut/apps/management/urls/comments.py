from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.note_comment',
    url(r'^$', 'list', name='management_comment_list'),
    url(r'^(?P<comment_id>\d+)/del/$', 'delete', name='management_comment_del'),
)

__author__ = 'edison'
