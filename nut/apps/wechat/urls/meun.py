from django.conf.urls import url, patterns
from apps.wechat.views.menu import MenuCreateView

urlpatterns = patterns(
    'apps.wechat.views.menu',
    url(r'^create/$', MenuCreateView.as_view(), name='wechat_menu_create'),
)
