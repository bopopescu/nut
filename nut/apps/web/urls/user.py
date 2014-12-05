from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.user',
    url(r'settings/$', 'settings', name='web_user_settings'),
)



__author__ = 'edison'
