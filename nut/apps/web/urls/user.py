from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.user',
    url(r'settings/$', 'settings', name='web_user_settings'),
    url(r'upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),
)



__author__ = 'edison'
