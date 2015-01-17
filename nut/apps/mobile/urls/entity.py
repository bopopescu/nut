from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.entity',
    url(r'^$', 'list', name='mobile_entity_list'),
    url(r'^guess/$', 'guess', name='mobile_entity_guess'),
    url(r'^(?P<entity_id>\d+)/$', 'detail', name='mobile_entity_detail'),
    # url(r'^note/$', 'note', name='mobile_entity_note'),

)

urlpatterns += patterns(
    'apps.mobile.views.note',
    url(r'^note/(?P<note_id>\d+)/$', 'detail', name='mobile_entity_note'),
)


__author__ = 'edison'
