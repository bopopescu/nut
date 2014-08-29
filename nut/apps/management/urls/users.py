from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.users',
    url(r'^$', 'list', name='management_user_list'),
    url(r'^(?P<user_id>\d+)/edit/$', 'edit', name='management_user_edit'),
    url(r'^(?P<user_id>\d+)/reset-password/$', 'reset_password', name='management_user_reset_password'),
    url(r'^(?P<user_id>\d+)/upload-avatar/$', 'upload_avatar', name='management_user_upload_avatar'),
    url(r'^(?P<user_id>\d+)/post/$', 'post', name='management_user_post'),
)

__author__ = 'edison'
