from django.conf.urls import url, patterns, include
from apps.v4.views import DiscoverView, HomeView, \
    AuthorizedUser, UnreadView, \
    TopPopularView, PopularView, APISearchView, APISearchHotWordView
from apps.v4.views.marketing import LaunchBoardView


urlpatterns = patterns(
    'apps.v4.views',
    url(r'^launchboard/$', LaunchBoardView.as_view(), name="v4_launch_board"),
    url(r'^launch/$', LaunchBoardView.as_view(), name="v4_launch"),
    url(r'^homepage/$', 'homepage', name='v4_homepage'),
    url(r'^home/$', HomeView.as_view(), name='v4_home'),
    url(r'^selection/$', 'selection', name='v4_selection'),

    # TODO: popular API
    url(r'^popular/$', PopularView.as_view(), name='v4_popular'),

    # TODO: discover API
    url(r'^discover/$', DiscoverView.as_view(), name='v4_discover'),


    url(r'^authorized/users/', AuthorizedUser.as_view(), name='v4_authorized_user'),

    url(r'^toppopular/$', TopPopularView.as_view(), name='v4_toppopular'),

    url(r'^unread/$', UnreadView.as_view(), name='v4_unread'),
    url(r'^item/(?P<item_id>\w+)/$', 'visit_item', name='v4_visit_item'),

    url(r'^apns/token/$', 'apns_token', name='v4_apns_token'),

# TODO: search API
    url(r'^search/$', APISearchView.as_view(), name='v4_search'),
    url(r'^search/keywords/$', APISearchHotWordView.as_view(), name='v4_search_hot_word'),
)

urlpatterns += patterns(
    'apps.v4.views.account',
    url(r'^login/$', 'login', name='v4_login'),
    url(r'^register/$', 'register', name='v4_register'),
    url(r'^logout/$', 'logout', name='v4_logout'),
    url(r'^forget/password/$', 'forget_password', name='v4_foreget_password'),

    url(r'^apns/token/$', 'apns_token', name='v4_apns_token'),

# TODO: weibo
    url(r'^sina/login/$', 'weibo.login_by_weibo', name="v4_login_by_weibo"),
    url(r'^sina/register/$', 'weibo.register_by_weibo', name='v4_register_by_weibo'),
    url(r'^sina/bind/$', 'weibo.link_by_weibo', name='v4_bind_by_weibo'),
    url(r'^sina/unbind/$', 'weibo.unlink_by_weibo', name='v4_unbind_by_weibo'),

# TODO: taobao
    url(r'^taobao/login/$', 'taobao.login_by_taobao', name='v4_login_by_taobao'),
    url(r'^taobao/register/$', 'taobao.register_by_taobao', name='v4_register_by_taobao'),

# TODO: new sign in or sign up by weibo
    url(r'^weibo/login/$', 'weibo.signin_by_weibo', name='v4_signin_by_weibo'),

# TODO: new sign in or sign up by Baichuan
    url(r'^baichuan/login/$', 'baichuan.login', name='v4_login_by_baichuan'),

# TODO: sign in or sign up by weChat
    url(r'^wechat/login/$', 'wechat.login', name='v4_login_by_wechat'),

)

urlpatterns += patterns(
    'apps.v4.views',
    url(r'^articles/', include('apps.v4.urls.articles')),

    url(r'^entity/', include('apps.v4.urls.entity')),
    url(r'^cart/', include('apps.v4.urls.cart')),
    url(r'^order/', include('apps.v4.urls.order')),

    url(r'^category/', include('apps.v4.urls.category')),
    url(r'^user/', include('apps.v4.urls.user')),
    url(r'^message/', include('apps.v4.urls.message')),
    url(r'^feed/', include('apps.v4.urls.feed')),
)

__author__ = 'edison7500'
