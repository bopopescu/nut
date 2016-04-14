from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.web.feeds import SelectionFeeds, ArticlesFeeds,ArticlesInterviewFeeds


urlpatterns = staticfiles_urlpatterns()

# temp enable admin , by Anchen

# from django.contrib import admin
# admin.autodiscover()
#
# urlpatterns += patterns('',
#     (r'^admin/', include(admin.site.urls)),
# )

# temp enable admin end , by Anchen


handler500 = 'apps.web.views.page_error'
handler404 = 'apps.web.views.webpage_not_found'
handler403 = 'apps.web.views.permission_denied'


urlpatterns += patterns(
    '',
    url(r'^403/$', 'django.views.defaults.permission_denied'),
    url(r'^404/$', 'apps.web.views.webpage_not_found'),
    url(r'^500/$', 'apps.web.views.page_error'),
    # (r'^visit_item/$', 'mobile.views.old_visit_item'),
)

# add by anchen, for local img function testing
if getattr(settings, 'LOCAL_IMG_DEBUG', None):
    urlpatterns += patterns(
        'apps.images',
        url(r'^(images|img|avatar)/', include('apps.images.urls')),
    )

urlpatterns += patterns('',

    url(r'^management/', include('apps.management.urls')),
    url(r'^mobile/v3/', include('apps.mobile.urls')),
    url(r'^mobile/v4/', include('apps.v4.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^wechat/', include('apps.wechat.urls')),
    url(r'^counter/', include('apps.counter.urls')),
    url(r'^tag/', include('apps.tag.urls')),

    url(r'^', include('apps.web.urls')),
)


# sitemap
'''
    guoku sitemap urls
'''
from apps.web.sitemaps import UserSitemap, \
    EntitySitemap, \
    TagSitemap, \
    CategorySitemap, \
    ArticleSitemap

sitemaps = {
    'user': UserSitemap,
    'entity': EntitySitemap,
    'tag': TagSitemap,
    'category': CategorySitemap,
    'article': ArticleSitemap,
}

urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    url(r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),

    url(r'^feed/selection/$', SelectionFeeds()),
    url(r'^feed/articles/$', ArticlesFeeds()),
    url(r'^feed/articles/interview/$', ArticlesInterviewFeeds()),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


# for personal domain function
# put this pattern at LAST!

from apps.web.views.user import UserIndex
urlpatterns += patterns('',
               url(r'^(?P<user_domain>\w+)/$',  UserIndex.as_view(), name='user_domain_link'),
               )

