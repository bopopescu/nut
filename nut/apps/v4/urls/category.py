from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.category',
    url(r'^$', 'category_list', name='mobile_category_list'),
    url(r'^(?P<category_id>\d+)/stat/$', 'stat', name='mobile_category_stat'),
    url(r'^(?P<category_id>\d+)/entity/$', 'entity', name='mobile_category_entity'),
    url(r'^(?P<category_id>\d+)/entity/note/$', 'entity_note', name='mobile_category_entity_note'),
    url(r'^(?P<category_id>\d+)/user/(?P<user_id>\d+)/like/$', 'user_like', name='mobile_category_user_like'),
)

__author__ = 'edison'
