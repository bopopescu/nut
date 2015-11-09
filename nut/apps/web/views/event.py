# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.template.base import TemplateDoesNotExist
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta

from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.models import Show_Event_Banner, Show_Editor_Recommendation, Event
from apps.core.models import  Entity, Entity_Like, Note
from apps.core.utils.http import JSONResponse
from apps.tag.models import Tags, Content_Tags

from hashlib import md5
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

def _fill_banners_into_event_list(event_list):
    for ev in event_list:
        ev.banner_urls = ev.banner.get_banner_urls_for_event(ev)
    return event_list

@require_http_methods(['GET'])
def elist(request, template='web/events/list.html'):
    _event_list = Event.objects.filter(event_status__is_published=True).order_by('-slug')
    _event_list = _fill_banners_into_event_list(_event_list)
    return render_to_response(template,
                              {
                                  'event_list': _event_list,
                              },
                              context_instance=RequestContext(request))


@require_http_methods(['GET'])
def event(request, slug, template='web/events/home'):
    _page_num = request.GET.get('p', 1)
    _slug = slug
    try:
        event = Event.objects.get(slug = _slug)
        template = template + '_%s.html' % _slug
    except Event.DoesNotExist:
        raise Http404

    try:
        loader.get_template(template)
    except TemplateDoesNotExist:
        template = "web/events/home.html"

    hash = md5(event.tag.encode('utf-8')).hexdigest()
    tag = Tags.objects.get(hash=hash)
    inner_qs = Content_Tags.objects.filter(tag=tag, target_content_type=24)\
               .values_list('target_object_id', flat=True).using('slave')
    log.info(inner_qs.query)
    _eid_list = Note.objects.filter(pk__in=list(inner_qs)).values_list('entity_id', flat=True).using('slave')

    _entity_list = Entity.objects.filter(id__in=list(set(_eid_list)), status=Entity.selection)\
                                 .filter(selection_entity__is_published=True, selection_entity__pub_time__lte=datetime.now())\
                                 .using('slave')


    # here is some dirty code for 1111 event
    top_entities_list = None
    top_entities_list_like = list()
    if event.toptag :
        top_tag_name = event.toptag

        try:
            top_tag = Tags.objects.get(name=top_tag_name)

            note_id_list = Content_Tags.objects\
                                           .filter(tag=top_tag,target_content_type_id=24)\
                                           .values_list("target_object_id", flat=True)\
                                           .using('slave')

            top_entities_id_list = Note.objects\
                                       .filter(pk__in=list(note_id_list ))\
                                       .values_list('entity_id', flat=True)\
                                       .using('slave')

            top_entities_list = Entity.objects\
                                 .filter(pk__in=list(top_entities_id_list))\
                                 .filter(selection_entity__is_published=True, selection_entity__pub_time__lte=datetime.now())\
                                 .using('slave')

            if request.user.is_authenticated():
                top_entities_list_like=Entity_Like.objects\
                                            .filter(entity_id__in=top_entities_list, user=request.user)\
                                            .values_list('entity_id', flat=True).using('slave')


        except Tags.DoesNotExist as e:
            pass


    _paginator = ExtentPaginator(_entity_list, 12)

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
        el = list(el) + list(top_entities_list_like)
        # el =

    _show_event_banners = Show_Event_Banner.objects.filter(event=event, position__gt=0)
    _show_editor_recommendations = Show_Editor_Recommendation.objects.filter(event=event, position__gt=0)

    if request.is_ajax():
        _ret = {
            'status' : 0,
            'msg' : '没有更多数据'
        }

        if _entity_list:
            log.info(_entities)
            _t = loader.get_template('web/events/partial/event_entity_list.html')
            try:
                _c = RequestContext(request, {
                    'user_entity_likes': el,
                    'entities': _entities,
                })

                _data = _t.render(_c)
            except Exception, e:
                log.error('render error', e.message)
                _data = list()

            _ret = {
                'status' : '1',
                'data' : _data
            }
        return JSONResponse(
                data=_ret,
                content_type='text/html; charset=utf-8',
        )


    # log.info('tag text %s', event.tag)
    return render_to_response(
        template,
        {
            'event': event,
            'top_entities':top_entities_list,
            'top_entities_like':top_entities_list_like,
            'tag_text': event.tag,
            'show_event_banners': _show_event_banners,
            'show_editor_recommendations': _show_editor_recommendations,
            'entities': _entities,
            'user_entity_likes': el,
            'from_app':request.GET.get('from','normal') == 'app'

        },
        context_instance=RequestContext(request)
    )




__author__ = 'edison'
