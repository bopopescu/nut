from django.conf.urls import url, include, patterns

from apps.counter.views import Counter, ArticleImageCounter

urlpatterns = patterns(
    'apps.counter.views',
    url(r'^$',Counter.as_view() ,name='backend_counter'),
    url(r'feed/article/(?P<aid>\d+)/guoku_banner.jpg', ArticleImageCounter.as_view(),name='article_image_count')
    )
