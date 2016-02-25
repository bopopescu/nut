# from django.shortcuts import render_to_response
from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
# import random
from django.db.models import Count
from apps.core.models import Entity, Entity_Like, Sub_Category,\
                             Selection_Article, GKUser
from django.utils.log import getLogger

log = getLogger('django')



class DiscoverView(TemplateResponseMixin, ContextMixin, View):
    template_name = "web/main/discover.html"

    def get(self, request):
        popular_list = Entity_Like.objects.popular_random()
        _entities = Entity.objects.filter(id__in=popular_list)
        el = list()
        if request.user.is_authenticated():
            el = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=list(_entities))

        # cids = Entity.objects.filter(pk__in=popular_list).annotate(dcount=Count('category')).values_list('category_id', flat=True)
        # _categories = Sub_Category.objects.filter(id__in=list(cids), status=True)
        _categories = Sub_Category.objects.popular_random()
        _selection_articles = Selection_Article.objects.discover()[:3]
        _recommended_user = GKUser.objects.recommended_user()[:8]

        log.info(_categories)
        context = {
            'entities':_entities,
            'user_entity_likes': el,
            'categories': _categories[:15],
            'selection_articles':_selection_articles,
            'recommended_user': _recommended_user
        }
        return self.render_to_response(context)

__author__ = 'edison'
