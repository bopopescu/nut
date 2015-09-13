from django.conf.urls import url, patterns

from apps.management.views.restful import SbbannerAppView,ArticleAppView, FLinkAppView

urlpatterns = patterns(
    '',
    url(r'^application/sbbanner/$', SbbannerAppView.as_view() , name='restful_app_sbbanner'),
    url(r'^application/article/$', ArticleAppView.as_view() , name='restful_app_article'),
    url(r'^application/flink/$', FLinkAppView.as_view() , name='restful_app_flink'),
)
