# from django.shortcuts import render_to_response
# from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.views.decorators.http import require_GET
from django.template import RequestContext, loader
# from django.template import loader

from django.views.generic import ListView
from braces.views import JSONResponseMixin, AjaxResponseMixin

from apps.core.models import Entity, Entity_Like, Selection_Entity, GKUser
from apps.tag.models import Tags
# from apps.web.forms.search import SearchForm
from apps.core.forms.search import GKSearchForm
from haystack.generic_views import SearchView
from apps.core.utils.http import JSONResponse


# from apps.web.utils.viewtools import get_paged_list
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
# from apps.tag.models import Content_Tags
from apps.core.models import Sub_Category
# import random

# from apps.notifications import notify
from django.utils.log import getLogger

log = getLogger('django')

from datetime import datetime


class SelectionEntityList(JSONResponseMixin, AjaxResponseMixin , ListView):
    template_name =  'web/main/selection.html'
    model = Entity
    paginate_by = 30
    paginator_class = Jpaginator

    def get_refresh_time(self):
        refresh_time = self.request.GET\
                                    .get('t',datetime.now()\
                                                     .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_entity_like_list(self,entities,request):
        el = []
        if request.user.is_authenticated():
            e = entities.values_list('id', flat=True)
            el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)
        return el

    def get_context_data(self, **kwargs):
        context = super(SelectionEntityList,self).get_context_data()
        selections = context['page_obj']
        context['refresh_datetime']  = self.get_refresh_time()
        el = list()
        if self.request.user.is_authenticated():
            # notify.send(request.user, recipient=request.user, verb='you visitor selection page')
            e = selections.object_list
            el = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=list(e.values_list('entity_id', flat=True))).using('slave')
        context['user_entity_likes'] = el
        context['selections'] = selections
        return context

    def get_like_list(self, entities):
        like_list = list()
        if not self.request.user.is_authenticated():
            return like_list
        else:
            like_list = self.get_entity_like_list(entities, self.request)
            return like_list

    def get_queryset(self):
        qs = Selection_Entity.objects.published_until(self.get_refresh_time())
        return qs

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = getattr(self , 'object_list' , self.get_queryset())
        context  = self.get_context_data()
        template = 'web/main/partial/selection_ajax.html'
        _t = loader.get_template(template)
        _c = RequestContext(
            request,
            context
        )
        _data = _t.render(_c)
        return JSONResponse(
            data={
                'data': _data,
                'status': 1,
            },
            content_type='text/html; charset=utf-8',
        )


class SiteMapView(ListView):
    template_name = 'web/main/sitemap.html'

    queryset = Sub_Category.objects.all()
    # def get_queryset(self):

#
# def popular(request, template='web/main/popular.html'):
#
#     popular_list = Entity_Like.objects.popular_random()
#     # random.sample(popular_list, 60)
#     # _entities = Entity.objects.filter(id__in=list(popular_list))
#     _entities = Entity.objects.filter(id__in=popular_list)
#     # log.info("popular %s" % len(_entities))
#     el = list()
#     if request.user.is_authenticated():
#         el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(_entities))
#
#     return render_to_response(
#         template,
#         {
#             'entities':_entities,
#             'user_entity_likes': el,
#         },
#         context_instance = RequestContext(request),
#     )

class PopularView(ListView):

    template_name = 'web/main/popular.html'
    http_method_names = ['get']

    # queryset = Entity_Like.objects.popular_random()
    def get_queryset(self):
        popular_list = Entity_Like.objects.popular_random()
        self.entities = Entity.objects.filter(id__in=popular_list)
        return self.entities

    def get_context_data(self, **kwargs):
        context = super(PopularView,self).get_context_data()
        el = list()
        if self.request.user.is_authenticated():
            el = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=list(self.entities))

        context.update(
            {
                'user_entity_likes':el,
            }
        )
        return context

    def get(self, request, *args, **kwargs):

        return super(PopularView, self).get(request, *args, **kwargs)


class GKSearchView(SearchView):

    form_class = GKSearchForm
    http_method_names = ['get']
    template_name = 'web/main/search.html'
    paginator_class = Jpaginator

    def form_valid(self, form):
        self.queryset = form.search()
        if 'u' in self.type:
            res = self.queryset.models(GKUser).order_by('-fans_count')
        elif 't' in self.type:
            res = self.queryset.models(Tags)
        else:
            res = self.queryset.models(Entity).order_by('-like_count')
        log.info(res)
        context = self.get_context_data(**{
            self.form_name: form,
            'query': form.cleaned_data.get(self.search_field),
            'object_list': res,
            'type': self.type,
            'entity_count': self.queryset.models(Entity).count(),
            'user_count': self.queryset.models(GKUser).count(),
            'tag_count': self.queryset.models(Tags).count(),
        })
        if self.type == "e" and self.request.user.is_authenticated():
            entity_id_list = map(lambda x : x.object.pk, context['page_obj'])
            # log.info(entity_id_list)
            el = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=entity_id_list)
            context.update({
                'user_entity_likes': el,
            })
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.type = request.GET.get('t', 'e')
        return super(GKSearchView, self).get(request, *args, **kwargs)


__author__ = 'edison'



