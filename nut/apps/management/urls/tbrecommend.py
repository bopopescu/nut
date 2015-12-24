from django.conf.urls import url, patterns
from apps.management.views.tbrecommend import RecommendView

urlpatterns = patterns(
    'apps.management.views.tbrecommend',

    url(r'^$', RecommendView.as_view(), name='tb_recommendation'),
)