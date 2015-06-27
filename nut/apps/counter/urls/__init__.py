from django.conf.urls import url, include, patterns

from apps.counter.views import Counter

urlpatterns = patterns(
    'apps.counter.views',
    url(r'^$',Counter.as_view() ,name='backend_counter'),
    )
