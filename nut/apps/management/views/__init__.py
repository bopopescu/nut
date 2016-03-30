from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import  login_required

from apps.core.models import Show_Banner, GKUser, Entity, Note, Entity_Like, Selection_Entity, Article
# from apps.core.utils.http import SuccessJsonResponse
# from apps.report.models import Selection
from apps.management.decorators import staff_only
from datetime import datetime, timedelta, date, time

from django.utils.log import getLogger
# import binascii

log = getLogger('django')
today = datetime.today()


@login_required
@staff_only
def dashboard(request, template='management/dashboard.html'):

    # range_date = now - timedelta(days=1)
    range_date = days_ago(1)
    like_count = Entity_Like.objects.filter(created_time__range=(range_date,
                                                                 today)).count()
    reg_count = GKUser.objects.filter(date_joined__range=(range_date.strftime("%Y-%m-%d"),
                                                                 today)).count()

    sel_count = Selection_Entity.objects.filter(is_published=True, pub_time__range=(range_date,
                                                                 today)).count()

    note_count = Note.objects.filter(post_time__range=(range_date,
                                                                 today)).count()
    authorized_authors  = GKUser.objects.authorized_author()
    yesterday_finish_detail = []
    for author in authorized_authors:
        finish_num = get_update(author)
        yesterday_finish_detail.append([author, author.profile.nickname, finish_num])



    # if request.is_ajax():
    #     res = {}
    #
    #
    #     query = "select id, group_id, count(*) as ccount from core_sub_category where id in \
	 #                (select category_id from core_entity where id in \
	 #                (select entity_id from core_selection_entity where pub_time between '%s' and '%s'))group by group_id;" % (range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
    #
    #     s_c = Sub_Category.objects.raw(query)
    #     # log.info(s_c.query)
    #     res['category'] = []
    #     # color = 0xF7464A
    #     # highlight = 0xFF5A5E
    #     for row in s_c:
    #         data = {
    #             'value':row.ccount,
    #             # 'color': hex(color).replace('0x', '#'),
    #             # 'highlight': hex(highlight).replace('0x', '#'),
    #             'label': row.title,
    #         }
    #         res['category'].append(data)
    #         # color = color - 100000
    #         # highlight = highlight - 100000
    #         #
    #         # log.info(hex(color))
    #
    #
    #     s_report = Selection.objects.filter(pub_date__range=(range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
    # # page = request.GET.get('page', 1)
    #     res['selection'] = []
    #     for row in s_report:
    #         res['selection'].append(row.toDict())
    #     # log.info(res)
    #     return SuccessJsonResponse(res)

    # innqs = Selection_Entity.objects.filter(pub_time__range=(range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
    # e = Entity.objects.filter(id__in=innqs).values_list('category', flat=True).distinct()
    # log.info(e)
    # show_banners = Show_Banner.objects.all()

    # selection_entity_list = Entity.objects.filter(status = Entity.selection)

    # paginator = Paginator(selection_entity_list, 30)
    #
    # try:
    #     selection_entities = paginator.page(page)
    # except InvalidPage:
    #     selection_entities = paginator.page(1)
    # except EmptyPage:
    #     raise Http404
    # entities = Entity.objects.all()[0:10]
    notes = Note.objects.exclude(status__lte=Note.remove).filter(user__is_active__gt=0).order_by("-post_time")[0:10]


    return render_to_response(template,
                                {
                                    'notes': notes,
                                    # 'entities': entities,
                                    'like_count': like_count,
                                    'reg_count': reg_count,
                                    'sel_count': sel_count,
                                    'note_count': note_count,
                                    # 'selection_entities': selection_entities,
                                    'yesterday_finish_detail': yesterday_finish_detail,
                                },
                                context_instance = RequestContext(request))


# @login_required
# @staff_only
# def

def get_update(author):

    yesterday_finish_num = Article.objects.filter(creator=author.id,
                                                  updated_datetime__range=(days_ago(1),today)).count()
    last_week_num = Article.objects.filter(creator=author.id, updated_datetime__range=(days_ago(7),today)).count()
    last_month_num = Article.objects.filter(creator=author.id, updated_datetime__range=(days_ago(30),today)).count()

    return yesterday_finish_num, last_week_num, last_month_num

def days_ago(days_num):
    return date.today() - timedelta(days=days_num)

__author__ = 'edison7500'
