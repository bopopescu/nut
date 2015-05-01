from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.v4.views',
    url(r'^homepage/$', 'homepage', name='v4_homepage'),
    url(r'^selection/$', 'selection', name='v4_selection'),
    url(r'^popular/$', 'popular', name='v4_popular'),
    url(r'^toppopular/$', 'toppopular', name='v4_toppopular'),

    url(r'^unread/$', 'unread', name='v4_unread'),
    url(r'^item/(?P<item_id>\w+)/$', 'visit_item', name='v4_visit_item'),
)

urlpatterns += patterns(
    'apps.v4.views.account',
    url(r'^login/$', 'login', name='v4_login'),
    url(r'^register/$', 'register', name='v4_register'),
    url(r'^logout/$', 'logout', name='v4_logout'),
    url(r'^forget/password/$', 'forget_password', name='v4_foreget_password'),
    # url(r'^apns/token/$', 'apns_token', name='mobile_apns_token'),

    url(r'^sina/login/$', 'weibo.login_by_weibo', name="v4_login_by_weibo"),
    url(r'^sina/register/$', 'weibo.register_by_weibo', name='v4_register_by_weibo'),
    url(r'^sina/bind/$', 'weibo.link_by_weibo', name='v4_bind_by_weibo'),
    url(r'^sina/unbind/$', 'weibo.unlink_by_weibo', name='v4_unbind_by_weibo'),


    url(r'^taobao/login/$', 'taobao.login_by_taobao', name='v4_login_by_taobao'),
    url(r'^taobao/register/$', 'taobao.register_by_taobao', name='v4_register_by_taobao')
    # url(r'')
)

urlpatterns += patterns(
    'apps.v4.views',
    url(r'^entity/', include('apps.v4.urls.entity')),
    url(r'^category/', include('apps.v4.urls.category')),
    url(r'^user/', include('apps.v4.urls.user')),
    url(r'^message/', include('apps.v4.urls.message')),
    url(r'^feed/', include('apps.v4.urls.feed')),
)

__author__ = 'edison7500'
