from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext
from django.template import loader

from apps.core.models import Entity, Entity_Like, Selection_Entity
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
# from apps.web.forms.search import EntitySearchForm
from apps.web.forms.search import SearchForm
from apps.core.utils.http import JSONResponse
from django.utils.log import getLogger


from apps.notifications import notify

log = getLogger('django')

from datetime import datetime

#
# def index(request):
#
#
#     return HttpResponse("OK")


@require_GET
def selection(request, template='web/main/selection.html'):


    _page = request.GET.get('p', 1)
    _refresh_datetime = request.GET.get('t', None)
    if _refresh_datetime is None:
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # log.info(_refresh_datetime)
    entity_list = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)
    # entity_list = Entity.objects.
    paginator = ExtentPaginator(entity_list, 30)
    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    el = list()
    if request.user.is_authenticated():
        # notify.send(request.user, recipient=request.user, verb='you visitor selection page')
        e = selections.object_list
        el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(e.values_list('entity_id', flat=True)))

    if request.is_ajax():
        template = 'web/main/partial/selection_ajax.html'
        _t = loader.get_template(template)
        _c = RequestContext(
            request,
            {
                'selections': selections,
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

    log.info(_refresh_datetime)
    return render_to_response(
        template,
        {
            'selections': selections,
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
        el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(_entities))

    return render_to_response(
        template,
        {
            'entities':_entities,
            'user_entity_likes': el,
        },
        context_instance = RequestContext(request),
    )

def search(request, template="web/main/search.html"):


    if request.method == 'GET':
        _type = request.GET.get('t', 'e')
        form = SearchForm(request.GET)
        if form.is_valid():
            _results = form.search()
            # log.info("result %s" % results.count())
            # for row in results:
            #     print row.id
            # log.info("type %s" % form.get_search_type())
            return render_to_response(
                template,
                {
                    'keyword': form.get_keyword(),
                    'results': _results,
                    'type': form.get_search_type(),
                },
                context_instance=RequestContext(request),
            )


# def category(request, template="web/main/category.html"):
#
#     return render_to_response(
#         template,
#
#     )



__author__ = 'edison'



