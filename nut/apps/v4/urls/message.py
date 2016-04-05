from django.conf.urls import url, patterns
from apps.v4.views.message import MessageView

urlpatterns = patterns(
    'apps.v4.views.message',

    url(r'^$', MessageView.as_view(), name='v4_user_message'),
)

__author__ = 'edison'
