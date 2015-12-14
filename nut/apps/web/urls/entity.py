from django.conf.urls import url, patterns
from apps.web.views.entity import gotoBuyView


urlpatterns = patterns(
    'apps.web.views.entity',
    url(r'^note/(?P<eid>\d+)/$', 'entity_post_note', name='web_post_entity_note'),
    url(r'^note/(?P<nid>\d+)/update/$', 'entity_update_note', name='web_update_entity_note'),
    url(r'^note/(?P<nid>\d+)/comment/$', 'entity_note_comment', name='web_entity_note_comment'),
    url(r'^note/comment/(?P<comment_id>\d+)/delete/$', 'entity_note_comment_delete', name='web_entity_note_comment_delete'),
    # url(r'^note/(?P<nid>\d+)/comment/$')


    url(r'^(?P<eid>\d+)/like/$', 'entity_like', name='web_entity_like'),
    url(r'^(?P<eid>\d+)/unlike/$', 'entity_unlike', name='web_entity_unlike'),

    url(r'^new/$', 'entity_create', name='web_entity_create'),
    url(r'^load/item/', 'entity_load', name='web_load_item_info'),
    url(r'^(?P<eid>\d+)/report/$', 'report', name='web_entity_report'),
    url(r'^go/(?P<buy_id>\d+)/', gotoBuyView.as_view(), name='web_entity_buy_url'),
)


__author__ = 'edison'
