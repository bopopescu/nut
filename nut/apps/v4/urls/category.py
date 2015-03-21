from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.v4.views.category',
    url(r'^$', 'category_list', name='v4_category_list'),
    url(r'^(?P<category_id>\d+)/stat/$', 'stat', name='v4_category_stat'),
    url(r'^(?P<category_id>\d+)/entity/$', 'entity', name='v4_category_entity'),
    url(r'^(?P<category_id>\d+)/entity/note/$', 'entity_note', name='v4_category_entity_note'),
    url(r'^(?P<category_id>\d+)/user/(?P<user_id>\d+)/like/$', 'user_like', name='v4_category_user_like'),
)

__author__ = 'edison'
