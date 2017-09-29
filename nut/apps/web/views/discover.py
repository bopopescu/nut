# coding=utf-8
from django.views.generic import ListView
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin

from apps.core.models import Entity, Entity_Like, Selection_Article, GKUser, Category


class DiscoverView(TemplateResponseMixin, ContextMixin, View):
    template_name = "web/main/discover.html"

    def get(self, request):
        popular_list = Entity_Like.objects.popular_random()
        _entities = Entity.objects.filter(id__in=popular_list)
        if request.user.is_authenticated():
            el = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=list(_entities))
        else:
            el = []

        context = {
            'entities': _entities,
            'user_entity_likes': el,
            'categories': Category.objects.filter(status=True),
            'selection_articles': Selection_Article.objects.discover()[:3],
            'recommended_user': GKUser.objects.recommended_user()[:20]
        }
        return self.render_to_response(context)


class RecommendUserView(ListView):
    template_name = 'web/main/recommend_user.html'
    context_object_name = 'recommend_users'

    def get_queryset(self):
        return GKUser.objects.recommended_user()
