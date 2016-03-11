from django.conf.urls import url, patterns

from apps.web.views.brand import BrandDetailView

urlpatterns = patterns(
    '',
    url(r'^$', BrandDetailView.as_view(), name='web_brand_detail')
)