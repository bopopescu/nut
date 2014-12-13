from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext
from django.template import loader

from apps.core.models import Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.web.forms.search import EntitySearchForm
from apps.core.utils.http import JSONResponse
from django.utils.log import getLogger

log = getLogger('django')

from datetime import datetime


def index(request):


    return HttpResponse("OK")


@require_GET
def selection(request, template='web/main/selection.html'):


    _page = request.GET.get('p', 1)
    _refresh_datetime = request.GET.get('t', None)
    if _refresh_datetime is None:
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    entity_list = Entity.objects.filter(status=Entity.selection, updated_time__lt=_refresh_datetime)
    paginator = ExtentPaginator(entity_list, 30)
    try:
        entities = paginator.page(_page)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        raise  Http404


    el = list()
    if request.user.is_authenticated():
        e = entities.object_list
        # log.info(e)
        el = Entity_Like.objects.filter(entity__in=list(e), user=request.user).values_list('entity_id', flat=True)

    log.info(el)

    if request.is_ajax():
        template = 'web/main/partial/selection_item_list.html'
        _t = loader.get_template(template)
        _c = RequestContext(
            request,
            {
                'entities': entities,
                'user_entity_likes': el,
            }
        )
        _data = _t.render(_c)
        return JSONResponse(
            data={
                'data': _data,
                'status': 1,
            },
            content_type='text/html; charset=utf-8',
        )

    # refresh_datetime = datetime.now()
    return render_to_response(
        template,
        {
            'entities': entities,
            'user_entity_likes': el,
            'refresh_datetime':_refresh_datetime,
            'paginator':paginator,
        },
        context_instance = RequestContext(request),
    )


def popular(request, template='web/main/popular.html'):

    popular = Entity_Like.objects.popular()

    _entities = Entity.objects.filter(id__in=list(popular))
    el = list()
    if request.user.is_authenticated():
        # e = entities.object_list
        # log.info(e)
        el = Entity_Like.objects.filter(entity__in=list(_entities), user=request.user).values_list('entity_id', flat=True)
        log.info(el)
    # from django.db.models import Count
    # el =  Entity_Like.objects.annotate(dcount=Count('entity')).values_list('entity_id', flat=True)
    # print el
    return render_to_response(
        template,
        {
            'entities':_entities,
            'user_entity_likes': el,
        },
        context_instance = RequestContext(request),
    )

def search(request, template="web/main/search.html"):

    form = EntitySearchForm(request.GET)
    results = form.search()

    return render_to_response(
        template,
        {

        },
        context_instance = RequestContext(request),
    )


# def category(request, template="web/main/category.html"):
#
#     return render_to_response(
#         template,
#
#     )



__author__ = 'edison'



