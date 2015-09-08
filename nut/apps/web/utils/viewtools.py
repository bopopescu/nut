# -*- coding: utf-8 -*-

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.models import  Entity_Like, Entity, Selection_Article, Category, Sidebar_Banner
from django.http import Http404


# pop_category =[
#     {
#         'id': 13,
#         'title':'女装'
#     }, {
#         'id': 14,
#         'title':'男装'
#     },{
#         'id': 24,
#         'title':'首饰'
#     },{
#         'id': 38,
#         'title':'宠物'
#     },{
#         'id': 22,
#         'title':'电脑办公'
#     },{
#         'id': 4,
#         'title':'室内装饰'
#     },{
#         'id': 1,
#         'title':'生活日用'
#     },{
#         'id': 6,
#         'title':'家电'
#     },{
#         'id': 10,
#         'title':'文具'
#     },{
#         'id': 11,
#         'title':'图书'
#     },{
#         'id': 2,
#         'title':'收纳洗晒'
#     },{
#         'id': 21,
#         'title':'数码配件'
#     },{
#         'id': 19,
#         'title':'运动健身'
#     },{
#         'id': 27,
#         'title':'摄影摄像'
#     },
# ]

def get_paged_list(the_list, page_num=1, item_per_page=24):
    paginator = ExtentPaginator(the_list, item_per_page)
    try:
        _entities = paginator.page(page_num)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    return _entities

# NOT ready
def get_entity_like_list(entity_list, request):
    el = []
    if request.user.is_authenticated():
        e = entity_list.object_list
        el = Entity_Like.objects.filter(entity_id__in=tuple(e), user=request.user).values_list('entity_id', flat=True)
    return el



def add_side_bar_context_data(context):
    # _pop_categories = Sub_Category.objects.popular_random()
    # remove _pop_tags , wait for tag system refactor over
    # _pop_tags = Entity_Tag.objects.popular_random()
    popular_list = Entity_Like.objects.popular_random()[:5]
    _pop_entities = Entity.objects.filter(id__in=popular_list)
    popular_articles = Selection_Article.objects.get_popular()[:5]


    context['pop_entities'] = _pop_entities
    context['pop_categories'] = Category.objects.filter(status=True)
    context['pop_articles'] = popular_articles
    # context['sidebar_banners'] = Sidebar_Banner.objects.active_sbbanners()

    return context