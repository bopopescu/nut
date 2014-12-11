from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext

from apps.core.models import Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.web.forms.search import EntitySearchForm
from django.utils.log import getLogger

log = getLogger('django')

def index(request):


    return HttpResponse("OK")


@require_GET
def selection(request, template='web/main/selection.html'):

    entity_list = Entity.objects.filter(status= Entity.selection)
    _page = request.GET.get('p', 1)

    paginator = ExtentPaginator(entity_list, 30)
    try:
        entities = paginator.page(_page)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        raise  Http404

    e = entities.object_list
    log.info(e)
    el = Entity_Like.objects.filter(entity__in=list(e), user=request.user).values_list('entity_id', flat=True)

    log.info(el)

    return render_to_response(
        template,
        {
            'entities': entities,
            'user_entity_likes': el,
        },
        context_instance = RequestContext(request),
    )


def popular(request, template='web/main/popular.html'):


    return render_to_response(
        template,
        {

        },

    )

def search(request, template="web/main/search.html"):

    form = EntitySearchForm(request.GET)
    results = form.search()

    return render_to_response(
        template,
        {

        },

    )


def category(request, template="web/main/category.html"):

    return render_to_response(
        template,

    )



__author__ = 'edison'



