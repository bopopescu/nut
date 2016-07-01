from apps.management.views.entity_like import EntityLikeView
import django.conf.urls


urlpatterns = django.conf.urls.patterns(
    'apps.management.views.entity_like',

    django.conf.urls.url(r'^entitylike/$', EntityLikeView.get_query),

)
