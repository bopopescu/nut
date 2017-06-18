from django.conf.urls import url, patterns
from apps.mobile.views.entity import APIEntitySearchView

urlpatterns = patterns(
    'apps.mobile.views.entity',
    url(r'^$', 'entity_list', name='mobile_entity_list'),
    url(r'^search/$', APIEntitySearchView.as_view(), name='mobile_entity_search'),
    url(r'^guess/$', 'guess', name='mobile_entity_guess'),
    url(r'^(?P<entity_id>\d+)/$', 'detail', name='mobile_entity_detail'),
    url(r'^(?P<entity_id>\d+)/like/(?P<target_status>\d+)/$', 'like_action', name='mobile_entity_like_action'),
    url(r'^(?P<entity_id>\d+)/purchase/$', 'purchase_action', name='mobile_entity_purchase_action'),

    url(r'^(?P<entity_id>\d+)/report/$', 'report', name='mobile_entity_report'),
)

urlpatterns += patterns(
    'apps.mobile.views.note',
    url(r'^note/(?P<note_id>\d+)/$', 'detail', name='mobile_entity_note'),
    url(r'(?P<entity_id>\w+)/add/note/$', 'post_note', name='mobile_post_note'),
    url(r'^note/(?P<note_id>\d+)/update/$', 'update_note', name='mobile_update_note'),
    url(r'^note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke', name='mobile_note_poke'),

    url(r'^note/(?P<note_id>\d+)/add/comment/$', 'post_comment', name='mobile_post_note_comment'),
    url(r'^note/(?P<note_id>\d+)/comment/(?P<comment_id>\d+)/del/$', 'del_comment', name='mobile_note_comment_del'),

    url(r'^note/(?P<note_id>\d+)/report/$', 'report', name='mobile_entity_note_report'),
)

__author__ = 'edison'
