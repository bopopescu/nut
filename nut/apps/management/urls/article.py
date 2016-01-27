from django.conf.urls import url, patterns
from apps.management.views.article import SelectionArticleList,\
    SelectionPendingArticleList, \
    EditSelectionArticle, \
    CreateSelectionArticle,\
    ArticleList,\
    DraftArticleList, \
    RemoveSelectionArticle,\
    UpdateArticleView,\
    AuthorArticleList




urlpatterns = patterns(
    'apps.management.views.article',
    url(r'^all/$',ArticleList.as_view() , name="management_article_list"),
    url(r'^draft/$', DraftArticleList.as_view(), name='management_article_draft'),
    url(r'^authorized_author/$', AuthorArticleList.as_view(), name='management_author_article_list'),
    url(r'^create/$', 'create', name="management_article_create"),
    url(r'^(?P<article_id>\d+)/edit/$', 'edit', name='management_article_edit'),

    url(r'^(?P<pk>\d+)/edit/new/$',UpdateArticleView.as_view(), name='management_article_edit_new'),

    url(r'^(?P<article_id>\d+)/cover/upload/$', 'upload_cover', name='management_article_cover_upload'),
    url(r'^(?P<article_id>\d+)/preview/$', 'preview', name='management_article_preview'),

    # by An , handle selection Article
    url(r'^selections/$', SelectionArticleList.as_view(), name='management_selection_article_list'),
    url(r'^selections/pending/$', SelectionPendingArticleList.as_view(), name='management_selection_pending_article_list'),
    url(r'^selections/(?P<sla_id>\d+)/edit/$', EditSelectionArticle.as_view(), name='management_selection_article_edit'),
    url(r'^(?P<article_id>\d+)/createselection/$',CreateSelectionArticle.as_view(), name='management_create_selection_article'),
    url(r'^(?P<selection_article_id>\d+)/removeselection/$',RemoveSelectionArticle.as_view(), name='management_remove_selection_article'),

)

__author__ = 'edison'
