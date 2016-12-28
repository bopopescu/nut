from django.conf.urls import url, patterns

from apps.seller.views.web import SellerView, TrendRedirectView, Seller2015RedirectView,\
                                  NewSellerView, ShopsView, TopicArticlesView, OpinionsView, ColumnsView

urlpatterns = patterns('',

            url(r'^$', TrendRedirectView.as_view(), name='web_trend'),
            url(r'^best-of-2015/$', SellerView.as_view(), name='year_store_2015'),
            url(r'^best-of-2016/$', NewSellerView.as_view(), name='year_store_2016'),
            url(r'^best-of-2016/stores/$', ShopsView.as_view(), name='year_store_2016_shops'),
            url(r'^best-of-2016/opinions/$', OpinionsView.as_view(), name='year_store_2016_opinions'),
            url(r'^best-of-2016/columns/$', OpinionsView.as_view(), name='year_store_2016_columns'),
            url(r'^best-of-2016/topics/$', TopicArticlesView.as_view(), name='year_store_2016_topics'),
            url(r'^best-of-2016/topics/(?P<tag_name>.*?)/$', TopicArticlesView.as_view(), name='topic_articles_url'),
        )