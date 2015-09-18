from django.conf.urls import url, patterns
from apps.v4.views.entity import APIEntitySearchView

urlpatterns = patterns(
    'apps.v4.views.entity',
    url(r'^$', 'entity_list', name='v4_entity_list'),
    url(r'^search/$', APIEntitySearchView.as_view(), name='v4_entity_search'),
    # url(r'^search/$', 'search', name='v4_entity_search'),
    url(r'^guess/$', 'guess', name='v4_entity_guess'),
    url(r'^(?P<entity_id>\d+)/$', 'detail', name='v4_entity_detail'),
    url(r'^(?P<entity_id>\d+)/like/(?P<target_status>\d+)/$', 'like_action', name='v4_entity_like_action'),

    url(r'^(?P<entity_id>\d+)/liker/$', 'entity_liker', name='v4_entity_liker'),

    # url(r'^note/$', 'note', name='v4_entity_note'),
    url(r'^(?P<entity_id>\d+)/report/$', 'report', name='v4_entity_report'),
)

urlpatterns += patterns(
    'apps.v4.views.note',
    url(r'^note/(?P<note_id>\d+)/$', 'detail', name='v4_entity_note'),
    url(r'(?P<entity_id>\w+)/add/note/$', 'post_note', name='v4_post_note'),
    url(r'^note/(?P<note_id>\d+)/update/$', 'update_note', name='v4_update_note'),
    url(r'^note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke', name='v4_note_poke'),
    url(r'^note/(?P<note_id>\d+)/del/$', 'remove', name='v4_note_del'),

    url(r'^note/(?P<note_id>\d+)/add/comment/$', 'post_comment', name='v4_post_note_comment'),
    url(r'^note/(?P<note_id>\d+)/comment/(?P<comment_id>\d+)/del/$', 'del_comment', name='v4_note_comment_del'),

    url(r'^note/(?P<note_id>\d+)/report/$', 'report', name='v4_entity_note_report'),
)

__author__ = 'edison'
