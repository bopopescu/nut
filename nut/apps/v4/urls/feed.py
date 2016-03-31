from django.conf.urls import url, patterns
from apps.v4.views.feed import ActivityView


urlpatterns = patterns(
    'apps.v4.views.feed',
    url(r'^$', ActivityView.as_view(), name='v4_user_activity'),
)

__author__ = 'edison'
