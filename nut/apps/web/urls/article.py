from django.conf.urls import url, patterns

from apps.web.views.article import  EditorDraftList,\
                                    EditorArticleCreate,\
                                    EditorArticleEdit,\
                                    ArticleDetail,\
                                    ArticleDelete,\
                                    ArticleRelated,\
                                    NewSelectionArticleList,\
                                    ArticleDig, ArticleUndig, \
                                    ArticleTextRankView, \
                                    ArticleRemarkCreate, ArticleRemarkDelete,\
                                    ArticleRedirectView

urlpatterns = patterns(
    'apps.web.views.article',
    url(r'^$', NewSelectionArticleList.as_view(), name='web_selection_articles'),
    # url(r'^list/$', NewSelectionArticleList.as_view(), name='web_selection_articles_new'),

    url(r'^edit/$', EditorDraftList.as_view(), name='web_editor_article_list'),
    url(r'^create/$', EditorArticleCreate.as_view(), name='web_editor_article_create'),
    url(r'^(?P<pk>\d+)/edit/$', EditorArticleEdit.as_view(), name='web_editor_article_edit'),
    url(r'^(?P<pk>\d+)/delete/$', ArticleDelete.as_view(), name='web_article_delete'),

    url(r'^(?P<pk>\d+)/dig/$', ArticleDig.as_view(), name='web_article_dig'),
    url(r'^(?P<pk>\d+)/undig/$', ArticleUndig.as_view(), name='web_article_undig'),


    # url(r'^(?P<pk>\d+)/slug/(?P<slug>.+)/$', ArticleDetail.as_view(), name='web_article_page_slug'),
    url(r'^(?P<pk>\d+)/$', ArticleDetail.as_view(), name='web_article_page'),
    url(r'^(?P<pk>\d+)/related/$', ArticleRelated.as_view(), name='web_article_related'),


    url(r'^(?P<pk>\d+)/textrank/$', ArticleTextRankView.as_view(), name='web_article_textrank'),

    url(r'^(?P<pk>\d+)/remark/$', ArticleRemarkCreate.as_view(), name='web_article_remark'),
    url(r'^(?P<pk>\d+)/remark/delete/$', ArticleRemarkDelete.as_view(), name='web_article_remark_delete'),

)

__author__ = 'edison'
