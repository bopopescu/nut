from django.conf.urls import url, include, patterns
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from apps.web.views import AboutView, JobsView, Agreement, FaqView, DownloadView, CooperateView,\
    ShopServiceView, FuGuListView
from apps.web.views.design_week import DesignWeekViewSet
from apps.web.views.discover import DiscoverView, RecommendUserView
from apps.web.views.entity import EntityCard, EntityLikersView, EntitySaleView, NewEntityDetailView
from apps.web.views.flink import FriendlyLinkListView
from apps.web.views.main import GKSearchView, PopularView, IndexView
from apps.web.views.main import SelectionEntityList, SiteMapView, IndexArticleTagView, IndexSelectionEntityTagView,\
    IndexHotEntityView

urlpatterns = patterns(
    'apps.web.views',
    url(r'^$', IndexView.as_view(), name='web_index'),
    url(r'^index_article_tag', IndexArticleTagView.as_view(), name='web_index_article_tag'),
    url(r'^index_selection_entity_tag', IndexSelectionEntityTagView.as_view(), name='web_index_selection_entity_tag'),
    url(r'^index_hot_entity', IndexHotEntityView.as_view(), name='web_index_hot_entity'),
    url(r'^selection/$', RedirectView.as_view(url='/selected/')),
    url(r'^m/selection/$', RedirectView.as_view(url='/selected/')),
    url(r'^selected/$', SelectionEntityList.as_view(), name='web_selection'),

    url(r'^popular/$', PopularView.as_view(), name='web_popular'),
    url(r'^discover/$', DiscoverView.as_view(), name='web_discover'),
    url(r'^discover/users/$', RecommendUserView.as_view(), name='web_recommend_users'),

    url(r'^search/?$', GKSearchView.as_view(), name='web_search'),

    url(r'^sitemap/$', SiteMapView.as_view(), name='web_sitemap_url'),

)

urlpatterns += patterns(
    'apps.web.views.entity',
    url(r'^m/detail/(?P<entity_hash>\w+)/$', 'wap_entity_detail', name='wap_detail'),
    url(r'^weixin/present/(?P<entity_id>\d+)/$', 'wechat_entity_detail', name='wechat_detail'),
    url(r'^tencent/detail/(?P<entity_hash>\w+)/$', 'tencent_entity_detail', name='tencent_detail'),
)

urlpatterns += patterns(
    'apps.web.views.entity',
    url(r'^detail/(?P<entity_hash>\w+)/$', NewEntityDetailView.as_view(), name='web_entity_detail'),
    url(r'^detail/(?P<entity_hash>\w+)/liker/$', EntityLikersView.as_view(), name='web_entity_likers_list'),
    url(r'^detail/(?P<entity_hash>\w+)/card/$', EntityCard.as_view(), name='web_entity_card'),
    url(r'^detail/(?P<entity_hash>\w+)/sale/$', EntitySaleView.as_view(), name='web_entity_sale'),
)

from apps.web.views.account import RegisterWizard
from apps.web.forms.account import UserSignUpForm, UserSignUpBioForm

RegisterForms = [
    ('register', UserSignUpForm),
    ('register-bio', UserSignUpBioForm),
]

# account
urlpatterns += patterns(
    'apps.web.views.account',
    url(r'^login/$', 'login', name='web_login'),
    url(r'^logout', 'logout', name='web_logout'),
    url(r'^register/$', RegisterWizard.as_view(RegisterForms), name='web_register'),

    url(r'^sina/login/$', 'weibo.login_by_sina', name="web_login_by_sina"),
    url(r'^sina/auth/$', 'weibo.auth_by_sina', name="web_auth_by_sina"),
    url(r'^sina/bind/$', 'weibo.bind', name='web_bind_by_weibo'),
    url(r'^sina/unbind/$', 'weibo.unbind', name='web_unbind_by_weibo'),

    url(r'^taobao/login/$', 'taobao.login_by_taobao', name='web_login_by_taobao'),
    url(r'^taobao/auth/$', 'taobao.auth_by_taobao', name='web_auth_by_taobao'),
    url(r'^taobao/bind/$', 'taobao.bind', name='web_bind_by_taobao'),
    url(r'^taobao/unbind/$', 'taobao.unbind', name='web_unbind_by_taobao'),

    url(r'^weixin/login/$', 'wechat.login_by_wechat', name='web_login_by_wechat'),
    url(r'^weixin/auth/$', 'wechat.auth_by_wechat', name='web_auth_by_wechat'),
    url(r'^weixin/bind/$', 'wechat.bind', name='web_bind_by_weixin'),
    url(r'^weixin/unbind/$', 'wechat.unbind', name='web_unbind_by_weixin'),
)

# static page
urlpatterns += patterns(
    'apps.web.views',

    url(r'^about/$', AboutView.as_view(), name='web_about'),
    url(r'^shopservice/$', ShopServiceView.as_view(), name='web_shop_service'),
    url(r'^cooperate/$', CooperateView.as_view(), name='web_cooperate'),
    url(r'^jobs/$', JobsView.as_view(), name='web_jobs'),
    url(r'^agreement/$', Agreement.as_view(), name='web_agreement'),
    url(r'^links/$', FriendlyLinkListView.as_view(), name='web_links'),
    url(r'^faq/$', FaqView.as_view(), name='web_faq'),
    url(r'^download/$', DownloadView.as_view(), name='web_download'),
    url(r'^download/ios/$', 'download_ios'),
)

router = DefaultRouter()
router.register(r'design_week/2016', DesignWeekViewSet, base_name="Entity")

# entity
urlpatterns += patterns(
    'apps.web.views',
    url(r'^message/', include('apps.notifications.urls')),
    url(r'^entity/', include('apps.web.urls.entity')),
    url(r'^note/', include('apps.web.urls.note')),
    url(r'^category/', include('apps.web.urls.category')),
    url(r'^account/', include('apps.web.urls.account')),
    url(r'^u/', include('apps.web.urls.user')),
    url(r'^event/', include('apps.web.urls.event')),
    url(r'^articles/', include('apps.web.urls.article')),
    url(r'^brand/', include('apps.web.urls.brand')),
    url(r'^store/', include('apps.shop.urls.web')),
    url(r'^payment/', include('apps.payment.urls.web')),
    url(r'^cart/', include('apps.order.urls.cart_web')),
    url(r'^orders/', include('apps.order.urls.order_web')),
    url(r'^checkout/', include('apps.web.urls.checkout')),
    url(r'^seller_management/', include('apps.web.urls.seller_management')),
    url(r'^offline_shop/', include('apps.offline_shop.urls')),
    url(r'^', include(router.urls))
)

# old url 301
from apps.web.views.category import OldCategory

urlpatterns += patterns(
    '',
    url(r'^c/(?P<cid>\d+)/$', OldCategory.as_view(), name='web_category_old_url'),
)

urlpatterns += patterns('',
                        url(r'^captcha/', include('captcha.urls')),
                        )

# for seller 2015 page and happy new year page
# this is temp, for single page app only
#  do not add more url here
from apps.seller.views.web import TrendRedirectView, Seller2015RedirectView
from apps.web.views import HappyNYView, FuGuView, MarketView

urlpatterns += patterns('',
                        url(r'^trends/', include('apps.seller.urls.web')),
                        url(r'^trend/', TrendRedirectView.as_view(), name='trend_redirect_alter'),
                        )

urlpatterns += patterns('',
                        url(r'^store2015/', Seller2015RedirectView.as_view(), name='year_store_2015_old'),
                        url(r'^hou/', HappyNYView.as_view(), name='new_year_2015'),
                        url(r'guokuselectedshops2016/list/', FuGuListView.as_view(), name='fu_gu_da_hui_2016_list'),
                        url(r'guokuselectedshops2016/', FuGuView.as_view(), name='fu_gu_da_hui_2016'),
                        url(r'guokumarket2016', MarketView.as_view(), name='market_2016')
                        )
