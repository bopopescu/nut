from django.conf.urls import url, patterns

from apps.web.views.brand import BrandDetailView

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', BrandDetailView.as_view(), name='web_brand_detail'),
    url(r'^(?P<pk>\d+)/(?P<order_by>[\w-]+)/$', BrandDetailView.as_view(), name='web_brand_detail'),
)
