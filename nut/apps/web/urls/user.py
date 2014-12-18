from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.user',
    url(r'settings/$', 'settings', name='web_user_settings'),
    url(r'upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),
    url(r'(?P<user_id>\d+)/note/', 'post_note', name='web_user_post_note'),
)



__author__ = 'edison'
