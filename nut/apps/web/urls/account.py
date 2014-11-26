from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.account',
    url(r'^forget-password/$', 'forget_password', name='web_forget_password'),
)

__author__ = 'edison7500'
