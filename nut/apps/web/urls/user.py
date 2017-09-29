# coding=utf-8
from django.conf.urls import url, patterns

from apps.web.views.user import ChangePasswdFormView
from apps.web.views.user import UserIndex, UserLikeView, UserNoteView, UserTagView, UserFansView, UserFollowingsView, \
    UserPublishedArticleView, UserPublishedSelectionArticleView, UserLikeArticleView, UserSendVerifyMail, \
    UserEntitiesView

urlpatterns = patterns(
    'apps.web.views.user',
    url(r'^settings/$', 'settings', name='web_user_settings'),
    url(r'^change/password/$', ChangePasswdFormView.as_view(), name='web_user_change_password'),
    url(r'^bind/sns/$', 'bind_sns', name='web_user_bind_sns'),
    url(r'^upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),
    url(r'^sendverifymail/$', UserSendVerifyMail.as_view(), name='web_user_mail_verify'),

    url(r'^(?P<user_id>\d+)/$', UserIndex.as_view(), name='web_user_index'),
    url(r'^(?P<user_id>\d+)/like/$', UserLikeView.as_view(), name='web_user_entity_like'),
    url(r'^(?P<user_id>\d+)/like/(?P<cid>\d+)/category/$', UserLikeView.as_view(),
        name='web_user_entity_like_by_category'),

    url(r'^(?P<user_id>\d+)/note/$', UserNoteView.as_view(), name='web_user_post_note'),
    url(r'^(?P<user_id>\d+)/tags/$', UserTagView.as_view(), name='web_user_tag'),

    url(r'^(?P<user_id>\d+)/articles/$', UserPublishedSelectionArticleView.as_view(), name='web_user_article'),

    url(r'^(?P<user_id>\d+)/articles/selection/$', UserPublishedSelectionArticleView.as_view(),
        name='web_user_article_selection'),
    url(r'^(?P<user_id>\d+)/articles/published/$', UserPublishedArticleView.as_view(),
        name='web_user_article_published'),
    # the list articles which the user likes
    url(r'^(?P<user_id>\d+)/articles/like/$', UserLikeArticleView.as_view(), name='web_user_article_like'),

    url(r'^(?P<user_id>\d+)/fans/$', UserFansView.as_view(), name='web_user_fans'),
    url(r'^(?P<user_id>\d+)/followings/$', UserFollowingsView.as_view(), name='web_user_followings'),

    url(r'^(?P<user_id>\d+)/tags/(?P<tag_name>\w+)/$', 'user_tag_detail', name='web_user_tag_detail'),
    # Azure thinks the user's goods link below is an abandon link.
    url(r'^(?P<user_id>\d+)/goods/$', 'user_goods', name='web_user_goods'),
    # create a goods link for seller
    url(r'^(?P<user_id>\d+)/entities/$', UserEntitiesView.as_view(), name='web_user_entities'),

    url(r'^(?P<user_id>\d+)/follow/$', 'follow_action', name='web_user_follow_action'),
    url(r'^(?P<user_id>\d+)/unfollow/$', 'unfollow_action', name='web_user_unfollow_action'),
)
