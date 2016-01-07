from django.conf.urls import url, include, patterns
from django.views.generic import RedirectView
from apps.web.views import AboutView, JobsView, Agreement, LinksView, FaqView, DownloadView
from apps.web.views.discover import DiscoverView
from apps.web.views.main import SelectionEntityList, SiteMapView
from apps.web.views.entity import EntityCard, EntityLikersView
from apps.web.views.main import GKSearchView, PopularView,IndexView
from apps.web.views.flink import FriendlyLinkListView

urlpatterns = patterns(
    'apps.web.views',
    # url(r'^$', 'main.index', name='web_index'),
    url(r'^$', RedirectView.as_view(url='/selected/'), name='web_home'),
    url(r'^index_test/$', IndexView.as_view(), name='web_index'),
    url(r'^selection/$', RedirectView.as_view(url='/selected/')),
    url(r'^selected/$', SelectionEntityList.as_view(), name='web_selection'),
    # url(r'^selected/$', 'main.selection', name='web_selection'),
    # url(r'^selected/$',  RedirectView.as_view(url='/selection/'),

    url(r'^popular/$', PopularView.as_view(), name='web_popular'),
    url(r'^discover/$', DiscoverView.as_view(), name='web_discover'),
    # url(r'^search/$', 'main.search', name='web_search'),
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

    url(r'^detail/(?P<entity_hash>\w+)/$', 'entity_detail', name='web_entity_detail'),
    url(r'^detail/(?P<entity_hash>\w+)/liker/$', EntityLikersView.as_view(), name='web_entity_likers_list'),
    url(r'^detail/(?P<entity_hash>\w+)/card/$', EntityCard.as_view() , name='web_entity_card'),

)


from apps.web.views.account import RegisterWizard
from apps.web.forms.account import UserSignUpForm, UserSignUpBioForm

RegisterForms = [
    ('register', UserSignUpForm),
    ('register-bio', UserSignUpBioForm),
]

#account
urlpatterns += patterns(
    'apps.web.views.account',
    url(r'^login/$', 'login', name='web_login'),
    # url(r'^register/$', 'register', name='web_register'),
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
    url(r'^jobs/$', JobsView.as_view(), name='web_jobs'),
    url(r'^agreement/$', Agreement.as_view(), name='web_agreement'),
    url(r'^links/$', FriendlyLinkListView.as_view(), name='web_links'),
    url(r'^faq/$', FaqView.as_view(), name='web_faq'),
    url(r'^download/$', DownloadView.as_view(), name='web_download'),
    url(r'^download/ios/$', 'download_ios'),
)

# entity
urlpatterns += patterns(
    'apps.web.views',
    url(r'^message/', include('apps.notifications.urls')),
    url(r'^entity/', include('apps.web.urls.entity')),
    url(r'^note/', include('apps.web.urls.note')),
    url(r'^category/', include('apps.web.urls.category')),
    # url(r'^c/', include('apps.web.urls.category')),
    url(r'^account/', include('apps.web.urls.account')),
    url(r'^u/', include('apps.web.urls.user')),
    url(r'^event/', include('apps.web.urls.event')),
    # url(r'^t/', include('apps.web.urls.tag')),
    # url(r'^tag/(?P<tag_text>\w+)/$', 'tag.text_to_detail', name='web_tag_text',),
    url(r'^articles/',include('apps.web.urls.article')),
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


from apps.seller.views.web import SellerView
urlpatterns += patterns('',
            url(r'^store2015/', SellerView.as_view(), name='year_store_2015'),
        )


__author__ = 'edison7500'