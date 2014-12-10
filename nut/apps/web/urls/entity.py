from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.entity',
    url(r'^(?P<entity_hash>\w+)/$', 'entity_detail', name='web_entity_detail'),
    url(r'^note/(?P<nid>\d+)/comment/$', 'entity_note_comment', name='web_entity_note_comment'),
)

__author__ = 'edison'
