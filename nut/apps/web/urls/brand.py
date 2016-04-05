from django.conf.urls import url, patterns

from apps.web.views.brand import BrandDetailView, BrandListView

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', BrandDetailView.as_view(), name='web_brand_detail'),
)