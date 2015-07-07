from django.conf.urls import url, patterns
from apps.management.views.buy_link import BuyLinkListView


urlpatterns = patterns(
    '',
    url(r'^$', BuyLinkListView.as_view(), name='buy_link_list'),
)


__author__ = 'edison'
