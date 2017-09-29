# coding=utf-8

from django.http import Http404

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import Entity_Like, Entity, Selection_Article, Category
from apps.site_banner.models import SiteBanner


def get_paged_list(the_list, page_num=1, item_per_page=24):
    paginator = ExtentPaginator(the_list, item_per_page)
    try:
        _entities = paginator.page(page_num)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    return _entities


def add_side_bar_context_data(context):
    popular_list = Entity_Like.objects.popular_random()[:5]
    _pop_entities = Entity.objects.filter(id__in=popular_list)
    popular_articles = Selection_Article.objects.get_popular()[:5]

    context['pop_entities'] = _pop_entities
    context['pop_categories'] = Category.objects.filter(status=True)
    context['pop_articles'] = popular_articles
    context['sidebar_banners'] = SiteBanner.objects.get_sidebar_banner()

    return context
