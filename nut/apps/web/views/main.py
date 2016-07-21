#encoding: utf-8
from datetime import datetime

from haystack.generic_views import SearchView
from braces.views import AjaxResponseMixin
from braces.views import JSONResponseMixin
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.utils.log import getLogger
from django.template import loader
from django.template import RequestContext
from django.core import exceptions
from django.core.cache import cache



from apps.core.tasks.recorder import record_search
from apps.core.utils.commons import get_client_ip, get_user_agent
from apps.tag.models import Tags, Content_Tags
from apps.core.models import Entity, Entity_Like, Category
from apps.core.models import Selection_Entity
from apps.core.models import GKUser
from apps.core.models import Show_Banner
from apps.core.models import Selection_Article
from apps.core.models import Article
from apps.core.forms.search import GKSearchForm
from apps.core.utils.http import JSONResponse
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.core.models import Sub_Category
from apps.shop.models import StorePageBanners
from apps.site_banner.models import SiteBanner

log = getLogger('django')


class IndexView(JSONResponseMixin, AjaxResponseMixin,TemplateView):
    template_name = 'web/index.html'

    def get_banners(self):
        shows = Show_Banner.objects.all()
        banners = []
        for show in shows:
            banners.append({
                'url': show.banner.url,
                'img': show.banner.image_url
            })
        return banners

    def get_selection_entities(self):
        selections = Selection_Entity.objects.published_until_now()\
                                     .select_related('entity').using('slave')
        return selections

    def get_selection_articles(self):
        articles = Selection_Article.objects.published_until()
        return articles

    def get_hot_categories(self):
        cates = Sub_Category.objects.popular_random(total=15)
        return cates

    def get_top_articles(self):
        return []

    def get_top_entities(self):
        return []

    def get_hot_entities(self):
        popular_list = Entity_Like.objects.popular_random()
        _hot_entities = Entity.objects.filter(id__in=popular_list)
        return _hot_entities

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['banners'] = SiteBanner.objects.get_mainpage_banner()  # 顶部banner (link, image)
        context['categories'] = Category.objects.filter(status=True)  # 品类
        popular_list = Entity_Like.objects.popular_random()
        context['entities'] = Entity.objects.filter(id__in=popular_list)  # 热门商品
        context['article_tags'] = Tags.objects.top_article_tags()  # 图文标签
        # context['articles'] = Selection_Article.objects.select_related('article').all()[:3]  # 最新精选图文
        context['articles'] = self.get_selection_articles()[:3]  # 最新精选图文
        # test = Selection_Article.objects\
        #                       .select_related('article').using('slave')
        context['recommand_users'] = GKUser.objects.recommended_user().select_related('profile')[:20]  # 推荐用户
        context['middle_banners'] = StorePageBanners.objects.filter(status=StorePageBanners.enabled)  # 中间banner
        # context['selection_entity'] = Selection_Entity.objects.select_related('entity')[:6]
        context['selection_entity'] = self.get_selection_entities()[:20]

        _entities = context['entities']
        if self.request.user.is_authenticated():
            context['user_entity_likes'] = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=
                list(_entities.values_list('id', flat=True))+(list(context['selection_entity'].values_list('entity_id',flat=True))))


        return context



class IndexArticleTagView(JSONResponseMixin, AjaxResponseMixin, ListView):
    def get_ajax(self, request, *args, **kwargs):
        context = {}
        tag_id = request.GET.get('dataValue')
        key = "index:article:tag:%s"%tag_id
        _data = cache.get(key)
        if not _data is None:
            return JSONResponse(
            data={
                'data': _data,
                'status': 1
            },
            content_type='text/html; charset=utf-8',
            )

        if tag_id == 'all':
            articles = Selection_Article.objects.published_until()[:3]
            context['articles'] = [item.article for item in articles]
        else:
            tag = Tags.objects.get(id=tag_id)
            article_ids = Content_Tags.objects.filter(tag=tag,
                                                 target_content_type_id=31).values_list(
                                                'target_object_id', flat=True)

            context['articles'] = Article.objects.filter(pk__in=article_ids,
                                  selections__is_published=True,
                                  selections__pub_time__lte=datetime.now())[:3]
        template = 'web/events/partial/new_event_article_item_ajax.html'
        _t = loader.get_template(template)
        _c = RequestContext(
            request,
            context
        )
        _data = _t.render(_c)

        cache.set(key , _data , timeout=3600*1)

        return JSONResponse(
            data={
                'data': _data,
                'status': 1
            },
            content_type='text/html; charset=utf-8',
        )

class IndexSelectionEntityTagView(JSONResponseMixin, AjaxResponseMixin, ListView):
    def get_ajax(self, request, *args, **kwargs):
        context = {}
        category_id = request.GET.get('dataValue')
        key = 'index:selection:entity:category:%s'%category_id
        _data = cache.get(key)
        if not _data is None:
            return JSONResponse(
            data={
                'data': _data,
                'status': 1
            },
            content_type='text/html; charset=utf-8',
            )


        if category_id == 'all':
            context['selection_entity'] = Selection_Entity.objects.published_until_now()[:20]
        else:
            sub_categories_ids = list(Sub_Category.objects.filter(group=category_id) \
                                      .values_list('id', flat=True))
            context['selection_entity'] = Selection_Entity.objects.published().filter(
                entity__category__in=sub_categories_ids)[:20]
        if self.request.user.is_authenticated():
            popular_list = Entity_Like.objects.popular_random()
            context['user_entity_likes'] = Entity_Like.objects.user_like_list(user=self.request.user, entity_list=
                list(Entity.objects.filter(id__in=popular_list).values_list('id', flat=True)) +
                list(context['selection_entity'].values_list('entity_id', flat=True)))

        template = 'web/main/partial/new_selection_ajax.html'
        _t = loader.get_template(template)
        _c = RequestContext(
            request,
            context
        )
        _data = _t.render(_c)
        cache.set(key, _data, timeout=15*60)
        return JSONResponse(
            data={
                'data': _data,
                'status': 1
            },
            content_type='text/html; charset=utf-8',
        )



class SelectionEntityList(JSONResponseMixin, AjaxResponseMixin, ListView):
    template_name = 'web/main/selection_new.html'
    model = Entity
    paginate_by = 40
    paginator_class = Jpaginator

    def get_refresh_time(self):
        refresh_time = self.request.GET \
            .get('t', datetime.now() \
                 .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_entity_like_list(self, entities, request):
        el = []
        if request.user.is_authenticated():
            e = entities.values_list('id', flat=True)
            el = Entity_Like.objects.filter(entity_id__in=tuple(e),
                                            user=request.user).values_list(
                'entity_id', flat=True)
        return el

    def get_context_data(self, **kwargs):
        context = super(SelectionEntityList, self).get_context_data()
        selections = context['page_obj']
        context['refresh_datetime'] = self.get_refresh_time()
        el = list()
        if self.request.user.is_authenticated():
            e = selections.object_list
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=list(
                                                        e.values_list(
                                                            'entity_id',
                                                            flat=True))
                                                    ).using('slave')
        context['user_entity_likes'] = el
        context['selections'] = selections                           #精选商品
        # context['banners'] = SiteBanner.objects.get_mainpage_banner()    #顶部banner (link, image)
        # context['categories'] = Category.objects.filter(status=True)     #品类
        # popular_list = Entity_Like.objects.popular_random()
        # context['entities'] = Entity.objects.filter(id__in=popular_list) #热门商品
        # context['article_tags'] = Tags.objects.top_article_tags()        #图文标签
        # context['articles'] = Selection_Article.objects.all()[:3]        #最新精选图文
        # context['recommand_users'] = GKUser.objects.recommended_user()[:20]    #推荐用户
        # context['middle_banners'] = StorePageBanners.objects.filter(status=StorePageBanners.enabled)    #中间banner
        return context

    def get_like_list(self, entities):
        like_list = list()
        if not self.request.user.is_authenticated():
            return like_list
        else:
            like_list = self.get_entity_like_list(entities, self.request)
            return like_list

    def get_queryset(self):
        try :
            qs = Selection_Entity.objects.published_until(self.get_refresh_time()) \
                .select_related('entity') \
                .prefetch_related('entity__likes')
        except exceptions.ValidationError as e :
            qs = Selection_Entity.objects.published_until() \
                .select_related('entity') \
                .prefetch_related('entity__likes')

        # prefetch notes will be a performance hit,
        # because top_note will use a filter , which will hit database again.

        return qs

    def get_ajax(self, request, *args, **kwargs):
        self.object_list = getattr(self, 'object_list', self.get_queryset())
        context = self.get_context_data()
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
                'status': 1
            },
            content_type='text/html; charset=utf-8',
        )


class SiteMapView(TemplateView):
    template_name = 'web/sitemap.html'


class PopularView(ListView):
    template_name = 'web/main/popular.html'
    http_method_names = ['get']

    # queryset = Entity_Like.objects.popular_random()
    def get_queryset(self):
        popular_list = Entity_Like.objects.popular_random()
        self.entities = Entity.objects.filter(id__in=popular_list)
        return self.entities

    def get_context_data(self, **kwargs):
        context = super(PopularView, self).get_context_data()
        el = list()
        if self.request.user.is_authenticated():
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=list(
                                                        self.entities))

        context.update(
            {
                'user_entity_likes': el,
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
        self.queryset = form.search(type=self.type)
        if 'u' in self.type:
            res = self.queryset.models(GKUser).order_by('-fans_count')
        elif 't' in self.type:
            res = self.queryset.models(Tags).order_by('-note_count')
        elif 'a' in self.type:
            res = self.queryset.models(Article).order_by('-score', '-read_count')
        else:
            res = self.queryset.models(Entity).order_by('-like_count')
        context = self.get_context_data(**{
            self.form_name: form,
            'query': form.cleaned_data.get(self.search_field),
            'object_list': res,
            'type': self.type,
            'entity_count': form.get_entity_count(),
            'user_count': form.get_user_count,
            'tag_count': form.get_tag_count(),
            'article_count': form.get_article_count(),
        })
        if self.type == "e" and self.request.user.is_authenticated():
            entity_id_list = map(lambda x: x.entity_id, context['page_obj'])
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=entity_id_list)
            context.update({
                'user_entity_likes': el,
            })
        key_words = form.cleaned_data.get(self.search_field)
        ip_address = get_client_ip(self.request)
        user_agent = get_user_agent(self.request)
        record_search(gk_user=self.request.user, key_words=key_words,
                      ip_address=ip_address, user_agent=user_agent)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.type = request.GET.get('t', 'e')
        return super(GKSearchView, self).get(request, *args, **kwargs)


__author__ = 'edison'
