from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext, loader
# from django.template import loader

from apps.core.models import Entity, Entity_Like, Selection_Entity, Entity_Tag
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
# from apps.web.forms.search import EntitySearchForm
from apps.web.forms.search import SearchForm
from apps.core.utils.http import JSONResponse
from django.utils.log import getLogger

from apps.web.utils.viewtools import get_paged_list

import random

# from apps.notifications import notify

log = getLogger('django')

from datetime import datetime


@require_GET
def selection(request, template='web/main/selection.html'):

    _page = request.GET.get('p', 1)
    _refresh_datetime = request.GET.get('t', None)
    if _refresh_datetime is None:
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # log.info(_refresh_datetime)
    entity_list = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime).using('slave')
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
        el = Entity_Like.objects.user_like_list(user=request.user, entity_list=list(e.values_list('entity_id', flat=True))).using('slave')

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

    # log.info(_refresh_datetime)
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

    popular_list = Entity_Like.objects.popular_random()
    # random.sample(popular_list, 60)
    # _entities = Entity.objects.filter(id__in=list(popular_list))
    _entities = Entity.objects.filter(id__in=popular_list)
    # log.info("popular %s" % len(_entities))
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


@require_GET
def search(request, template="web/main/search.html"):
    # if request.method == 'GET':
    _type = request.GET.get('t', 'e')
    _page = request.GET.get('page', 1)
    _order = request.GET.get('o', 'time')
    form = SearchForm(request.GET)

    if form.is_valid():
        _results = form.search()
        _objects = get_paged_list(_results , _page , 24)

        if _type == "t":
            tag_id_list = list()
            for row in _objects:
                log.info(row.id)
                tag_id_list.append(row.id)
            _results = Entity_Tag.objects.tags(tag_id_list)
            log.info(_results)

        c = {
                'keyword': form.get_keyword(),
                'results': _results,
                'type': _type,
                'objects': _objects,
                'entity_count': form.get_entity_count(),
                'user_count': form.get_user_count(),
                'tag_count': form.get_tag_count()
        }
        if _type == "e" and request.user.is_authenticated():

            entity_id_list = map(lambda x : int(x.id), _results)
            log.info(entity_id_list)
            el = Entity_Like.objects.user_like_list(user=request.user, entity_list=entity_id_list)
            c['user_entity_likes'] = el

        t = loader.get_template(template)
        c = RequestContext(request, c)
        return HttpResponse(t.render(c))


__author__ = 'edison'



