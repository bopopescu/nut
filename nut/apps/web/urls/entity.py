from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.entity',
    url(r'^(?P<entity_hash>\w+)/$', 'entity_detail', name='web_entity_detail'),
    url(r'^note/(?P<nid>\d+)/comment/$', 'entity_note_comment', name='web_entity_note_comment'),
    url(r'^note/comment/(?P<comment_id>\d+)/delete/$', 'entity_note_comment_delete', name='web_entity_note_comment_delete'),
    # url(r'^note/(?P<nid>\d+)/comment/$')
    url(r'^(?P<eid>\d+)/like/$', 'entity_like', name='web_entity_like'),
    url(r'^(?P<eid>\d+)/unlike/$', 'entity_unlike', name='web_entity_unlike'),
)

__author__ = 'edison'
