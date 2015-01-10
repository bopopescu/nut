# coding=utf-8
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from apps.core.models import Show_Event_Banner, Show_Editor_Recommendation, Event
from apps.core.models import Tag, Entity, Entity_Like

# from base.models import NoteSelection, Show_Event_Banner, Show_Editor_Recommendation, Event
# from base.note import Note
# from base.entity import Entity
# from base.tag import Tag
# from base.user import User
# from base.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
# from web.forms.account import SignInAccountForm
# # from utils.paginator import Paginator
# from utils.http import JSONResponse

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
def event(request, slug, template='events/home'):
    _slug = slug
    try:
        event = Event.objects.get(slug = _slug)
        template = template + '_%s.html' % _slug
    except Event.DoesNotExist:
        raise Http404

    if request.user.is_authenticated():
        # _request_user_id = request.user.id
        _request_user_context = User(request.user.id).read()
        _request_user_like_entity_set = Entity.like_set_of_user(request.user.id)
    else:
        # _request_user_id = None
        _request_user_context = None
        _request_user_like_entity_set = []


    _tag_text = Tag.get_tag_text_from_hash(event.tag)

    _entity_id_list = Tag.find_tag_entity(event.tag) # 双十一标签 hash
    log.info(_entity_id_list)
    _page_num = request.GET.get('p', 1)
    # _paginator = Paginator(_page_num, 24, len(_entity_id_list))


    # _entities = []
    # for _entity_id in _entity_id_list[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]:
    #     try:
    #         _entity_context = Entity(_entity_id).read()
    #         _entity_context['is_user_already_like'] = True if _entity_id in _request_user_like_entity_set else False
    #         _entities.append(_entity_context)
    #     except Exception, e:
    #         log.error(e.message)
    #
    #
    # log.info(_entities)
    # _page_num = request.GET.get('p', 1)
    _time_filter  = request.GET.get('t', datetime.now())
    _hdl = NoteSelection.objects.filter(post_time__lt = _time_filter, entity_id__in=_entity_id_list)
    _hdl.order_by('-post_time')

    _paginator = ExtentPaginator(_hdl, 30)
    # _paginator = ExtentPaginator(_page_num, 30, _hdl)
    # _note_selection_list = _hdl[_paginator.offset : _paginator.offset + _paginator.count_in_one_page]
    try:
        _note_selection_list = _paginator.page(_page_num)
    except PageNotAnInteger:
        _note_selection_list = _paginator.page(1)
    except Exception, e:
        log.error("Error: %s" % e.message)
        raise Http404

    # log.info(_note_selection_list)
    _selection_list = []
    # _entity_id_list = []
    for _note_selection in _note_selection_list:
        try:
            _selection_note_id = _note_selection['note_id']
            _entity_id = _note_selection['entity_id']
            _entity_context = Entity(_entity_id).read()
            _note = Note(_selection_note_id)
            _note_context = _note.read()
            _creator_context = User(_note_context['creator_id']).read()
            _is_user_already_like = True if _entity_id in _request_user_like_entity_set else False
            _selection_list.append(
                {
                    'is_user_already_like': _is_user_already_like,
                    'entity_context': _entity_context,
                    'note_context': _note_context,
                    'creator_context': _creator_context,
                }
            )
            _entity_id_list.append(_entity_id)
        except Exception, e:
            log.error(e.message)

    # log.info(_selection_list)

    _show_event_banners = Show_Event_Banner.objects.filter(event=event, position__gt=0)
    _show_editor_recommendations = Show_Editor_Recommendation.objects.filter(event=event, position__gt=0)

    if request.is_ajax():
        _ret = {
            'status' : 0,
            'msg' : '没有更多数据'
        }

        if _selection_list:
            _t = loader.get_template('main/partial/selection_item_list.html')
            _c = RequestContext(request, {
                'selection_list': _selection_list,
            })
            _data = _t.render(_c)

            _ret = {
                'status' : '1',
                'data' : _data
            }
        return JSONResponse(data=_ret)

    log.info('tag text %s', _tag_text)
    return render_to_response(
        template,
        {
            'event': event,
            'tag_text': _tag_text,
            'show_event_banners': _show_event_banners,
            'show_editor_recommendations': _show_editor_recommendations,
            'paginator': _paginator,
            'page_num' : _page_num,
                # 'curr_category_id' : _category_id,
            'user_context' : _request_user_context,
                # 'category_list' : _old_category_list,
            'selection_list' : _selection_list,
            # "entities": _entities,
            # "paginator" : _paginator
        },
        context_instance=RequestContext(request)
    )




__author__ = 'edison'
