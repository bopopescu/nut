from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.note_comment',
    url(r'^$', 'list', name='management_comment_list'),
)

__author__ = 'edison'
