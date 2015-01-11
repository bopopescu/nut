# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.models import Show_Event_Banner, Show_Editor_Recommendation, Event
from apps.core.models import Tag, Entity, Entity_Like, Entity_Tag
from apps.core.utils.http import JSONResponse
from datetime import datetime



from django.utils.log import getLogger
log = getLogger('django')


@require_http_methods(['GET'])
def home(request):
    events = Event.objects.filter(status = True)
    if len(events) > 0:
        event = events[0]
        return HttpResponseRedirect(reverse('web_event', args=[event.slug]))
    raise Http404

@require_http_methods(['GET'])
def event(request, slug, template='web/events/home'):
    _page_num = request.GET.get('p', 1)
    _slug = slug
    try:
        event = Event.objects.get(slug = _slug)
        template = template + '_%s.html' % _slug
    except Event.DoesNotExist:
        raise Http404

    tag = Tag.objects.get(tag_hash=event.tag)
    inner_qs = Entity_Tag.objects.filter(tag=tag).values_list('entity_id', flat=True)

    _entity_list = Entity.objects.filter(id__in=inner_qs, status=Entity.selection)
    # log.info(entities)
    # _page_num = request.GET.get('p', 1)
    # _paginator = Paginator(_page_num, 24, len(_entity_id_list))

    _paginator = ExtentPaginator(_entity_list, 30)

    try:
        _entities = _paginator.page(_page_num)
    except PageNotAnInteger:
        _entities = _paginator.page(1)
    except EmptyPage:
        raise Http404


    el = list()
    if request.user.is_authenticated():
        e = _entities.object_list
        el = Entity_Like.objects.filter(entity_id__in=list(e), user=request.user).values_list('entity_id', flat=True)
        # el =


    _show_event_banners = Show_Event_Banner.objects.filter(event=event, position__gt=0)
    _show_editor_recommendations = Show_Editor_Recommendation.objects.filter(event=event, position__gt=0)

    if request.is_ajax():
        _ret = {
            'status' : 0,
            'msg' : '没有更多数据'
        }

        if _entity_list:
            _t = loader.get_template('web/main/partial/selection_item_list.html')
            _c = RequestContext(request, {
                'user_entity_likes': el,
                'entities': _entities,
            })
            _data = _t.render(_c)

            _ret = {
                'status' : '1',
                'data' : _data
            }
        return JSONResponse(
                data=_ret,
                content_type='text/html; charset=utf-8',
        )

    log.info('tag text %s', event.tag)
    return render_to_response(
        template,
        {
            'event': event,
            'tag_text': tag.tag,
            'show_event_banners': _show_event_banners,
            'show_editor_recommendations': _show_editor_recommendations,
            'entities': _entities,
            'user_entity_likes': el,
        },
        context_instance=RequestContext(request)
    )




__author__ = 'edison'
