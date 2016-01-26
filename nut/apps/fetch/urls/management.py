from django.conf.urls import url, patterns
from apps.fetch.views.management import AddCookieView,CookieListView


urlpatterns = patterns(
    'apps.seller.views.management',
    url(r'^addcookie/$', AddCookieView.as_view() , name="management_add_sogou_cookie"),
    url(r'^cookielist/$', CookieListView.as_view() , name="management_cookie_list"),

)