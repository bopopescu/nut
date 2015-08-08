from django.conf.urls import url, patterns

from apps.web.views.user import UserIndex,\
                                UserLikeView, UserNoteView,\
                                UserTagView, UserArticleView,\
                                UserFansView, UserFollowingsView


urlpatterns = patterns(
    'apps.web.views.user',
    url(r'^settings/$', 'settings', name='web_user_settings'),
    url(r'^change/password/$', 'change_password', name='web_user_change_password'),
    url(r'^bind/sns/$', 'bind_sns', name='web_user_bind_sns'),
    url(r'^upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),

    # tmpl user page

    url(r'^(?P<user_id>\d+)/$', UserIndex.as_view(), name='web_user_index'),
    url(r'^(?P<user_id>\d+)/like/$', UserLikeView.as_view(), name='web_user_entity_like'),
    url(r'^(?P<user_id>\d+)/note/$', UserNoteView.as_view(), name='web_user_post_note'),
    url(r'^(?P<user_id>\d+)/tags/$', UserTagView.as_view(), name='web_user_tag'),
    url(r'^(?P<user_id>\d+)/articles/$', UserArticleView.as_view(), name='web_user_article'),
    url(r'^(?P<user_id>\d+)/fans/$', UserFansView.as_view(), name='web_user_fans'),
    url(r'^(?P<user_id>\d+)/followings/$', UserFollowingsView.as_view(), name='web_user_followings'),

    # url(r'^(?P<user_id>\d+)/new_front/$', UserIndex.as_view(), name='web_user_index_new'),
    # url(r'^(?P<user_id>\d+)/like/new_front/$', UserLikeView.as_view(), name='web_user_entity_like_new'),
    # url(r'^(?P<user_id>\d+)/note/new_front/$', UserNoteView.as_view(), name='web_user_post_note_new'),
    # url(r'^(?P<user_id>\d+)/tags/new_front/$', UserTagView.as_view(), name='web_user_tag_new'),
    # url(r'^(?P<user_id>\d+)/articles/new_front/$', UserArticleView.as_view(), name='web_user_article_new'),
    # url(r'^(?P<user_id>\d+)/fans/new_front/$', UserFansView.as_view(), name='web_user_fans_new'),
    # url(r'^(?P<user_id>\d+)/followings/new_front/$', UserFollowingsView.as_view(), name='web_user_followings_new'),

    # url(r'^(?P<user_id>\d+)/$',      'index', name='web_user_index' ),
    # url(r'^(?P<user_id>\d+)/like/$', 'entity_like', name='web_user_entity_like'),
    # url(r'^(?P<user_id>\d+)/note/$', 'post_note', name='web_user_post_note'),
    # url(r'^(?P<user_id>\d+)/tags/$', 'tag', name='web_user_tag'),
    # url(r'^(?P<user_id>\d+)/articles/$', 'articles', name='web_user_article'),
    url(r'^(?P<user_id>\d+)/tags/(?P<tag_name>\w+)/$', 'user_tag_detail', name='web_user_tag_detail'),
    # url(r'^(?P<user_id>\d+)/fans/$', 'fans', name='web_user_fans'),
    # url(r'^(?P<user_id>\d+)/followings/$', 'following', name='web_user_followings'),

    url(r'^(?P<user_id>\d+)/goods/$', 'user_goods', name='web_user_goods'),


    url(r'^(?P<user_id>\d+)/follow/$', 'follow_action', name='web_user_follow_action'),
    url(r'^(?P<user_id>\d+)/unfollow/$', 'unfollow_action', name='web_user_unfollow_action'),
)



__author__ = 'edison'
