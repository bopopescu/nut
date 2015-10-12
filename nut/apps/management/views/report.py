from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.report.models import Report


def report_list(request, template="management/report/list.html"):

    _page = request.GET.get('page', 1)

    _report_list = Report.objects.all().order_by("-id")

    paginator = ExtentPaginator(_report_list, 20)

    try:
        _reports = paginator.page(_page)
    except PageNotAnInteger:
        _reports = paginator.page(1)
    except EmptyPage:
        raise Http404


    return render_to_response(
        template,
        {
            'reports':_reports
        },
        context_instance = RequestContext(request),
    )


__author__ = 'edison'
