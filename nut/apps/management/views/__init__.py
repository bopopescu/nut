from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import  login_required

from apps.core.models import Show_Banner, Entity, Selection_Entity
from apps.core.utils.http import SuccessJsonResponse
from apps.report.models import Selection
from apps.management.decorators import staff_only
from datetime import datetime, timedelta

from django.utils.log import getLogger

log = getLogger('django')


@login_required
@staff_only
def dashboard(request, template='management/dashboard.html'):
    if request.is_ajax():
        now = datetime.now()
        range_date = now - timedelta(days=7)
        s_report = Selection.objects.filter(pub_date__range=(range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
    # page = request.GET.get('page', 1)
        res = []
        for row in s_report:
            res.append(row.toDict())
        log.info(res)
        return SuccessJsonResponse(res)


    show_banners = Show_Banner.objects.all()

    # selection_entity_list = Entity.objects.filter(status = Entity.selection)

    # paginator = Paginator(selection_entity_list, 30)
    #
    # try:
    #     selection_entities = paginator.page(page)
    # except InvalidPage:
    #     selection_entities = paginator.page(1)
    # except EmptyPage:
    #     raise Http404


    return render_to_response(template,
                                {
                                    'show_banners': show_banners,
                                    # 'selection_entities': selection_entities,
                                },
                                context_instance = RequestContext(request))


# @login_required
# @staff_only
# def

__author__ = 'edison7500'
