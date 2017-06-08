#coding=utf-8
from django.http import HttpResponseRedirect

from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Show_Banner, Banner, Buy_Link, Selection_Entity, Entity, Entity_Like, Sub_Category
from apps.core.utils.taobaoapi.utils import taobaoke_mobile_item_convert
# from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import random


from django.utils.log import getLogger
log = getLogger('django')


def is_taobaoke_url(url):
    return "s.click.taobao.com" in url

def get_taobao_url(taobao_id, is_mobile = False, app_key = None):
    url = ""
    if is_mobile:
        url = "http://a.m.taobao.com/i%s.htm" % taobao_id
    else:
        url = "http://item.taobao.com/item.htm?id=%s" % taobao_id
        if app_key:
            url += "&spm=2014.%s.0.0" % app_key
    return url

def decorate_taobao_url(url, ttid=None, sid=None, outer_code=None, sche=None):
    if sche:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sche=%s" % sche
    if ttid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&ttid=%s" % ttid
    if sid:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&sid=%s" % sid
    if is_taobaoke_url(url) and outer_code:
        question_mark = "" if "?" in url else "?"
        url += question_mark + "&unid=%s" % outer_code

    return url


@check_sign
def homepage(request):

    res = dict()

    # shows = Show_Banner.objects.all().values_list('banner_id', flat=True)
    # log.info(innqs)
    # banners = Banner.objects.filter(id__in=innqs)
    shows = Show_Banner.objects.all()
    res['banner'] = []
    for row in shows:
        res['banner'].append(
            {
                'url':row.banner.url,
                'img':row.banner.image_url
            }
        )

    res['discover'] = []
    # from django.db.models import Count
    # el = Entity_Like.objects.popular(scale='weekly')
    # category = Entity.objects.filter(pk__in=list(el)).annotate(dcount=Count('category')).values_list('category_id', flat=True)
    sub_category = Sub_Category.objects.popular_random(12)
    log.info(sub_category)
    for c in sub_category:
        res['discover'].append(
            c.v3_toDict()
        )
    # log.info(res['discover'])
    res['hottag'] = []

    res['config'] = {}
    res['config']['taobao_ban_count'] = 2
    res['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']
    return SuccessJsonResponse(data=res)


@check_sign
def selection(request):
    log.info(request.GET)
    # _timestamp = request.GET.get('timestamp', None)
    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _key = request.GET.get('session')


    _rcat = request.GET.get('rcat', None)
    log.info("rcat %s" % _rcat)

    if _rcat == '1':
        innqs = Sub_Category.objects.map(group_id_list=[13, 15, 17])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '2':
        # innqs = Sub_Category.objects.filter(group_id__in=[14, 16]).values_list('id', flat=True)
        innqs = Sub_Category.objects.map(group_id_list=[14, 16])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '3':
        innqs = Sub_Category.objects.map(group_id_list=[26, 28, 29, 30, 31, 32, 34, 35, 36])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '4':
        innqs = Sub_Category.objects.map(group_id_list=[9, 18, 24])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '5':
        innqs = Sub_Category.objects.map(group_id_list=[8, 33])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '6':
        innqs = Sub_Category.objects.map(group_id_list=[21, 22])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '7':
        innqs = Sub_Category.objects.map(group_id_list=[1, 2, 3, 4, 5, 6, 7, 41])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '8':
        innqs = Sub_Category.objects.map(group_id_list=[19, 20])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '9':
        innqs = Sub_Category.objects.map(group_id_list=[10, 11])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '10':
        innqs = Sub_Category.objects.map(group_id_list=[12, 40])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    elif _rcat == '11':
        innqs = Sub_Category.objects.map(group_id_list=[25, 38, 39])
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp, entity__category__in=innqs)[:30]
    else:
        selections = Selection_Entity.objects.published().filter(pub_time__lt=_timestamp)[:30]
    ids = selections.values_list('entity_id', flat=True)



    try:
        _session = Session_Key.objects.get(session_key=_key)
        # log.info("session %s" % _session)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(ids))
        log.info(_session.session_key)
        Selection_Entity.objects.set_user_refresh_datetime(session=_session.session_key)
    except Session_Key.DoesNotExist, e:
        # log.info(e.message)
        el = None
    # log.info(el)
    res = list()

    for selection in selections:
        # TODO： 解决entity可能没有top_note的问题
        if not selection.entity.top_note:
            continue
        r = {
            'entity':selection.entity.v3_toDict(user_like_list=el),
            'note':selection.entity.top_note.v3_toDict(),
        }

        res.append({
            'content': r,
            'post_time': selection.publish_timestamp,
            'type': "note_selection",
        })

    # paginator = ExtentPaginator(entity_list)
    return SuccessJsonResponse(res)


@check_sign
def popular(request):

    _scale = request.GET.get('scale', 'daily')
    _key = request.GET.get('session')
    log.info(_scale)
    popular_list = Entity_Like.objects.popular_random(_scale)
    _entities = Entity.objects.filter(id__in=popular_list, status=Entity.selection)

    try:
        _session = Session_Key.objects.get(session_key=_key)
        # log.info("session %s" % _session)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=_entities)
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = None


    res = dict()
    res['content'] = list()
    res['scale'] = _scale
    for e in _entities:
        r = {
            'entity': e.v3_toDict(user_like_list=el)
        }
        res['content'].append(r)

    return SuccessJsonResponse(res)


@check_sign
def unread(request):

    _key = request.GET.get('session')

    try:
        _session = Session_Key.objects.get(session_key = _key)
    except Session_Key.DoesNotExist:
        return ErrorJsonResponse(status=400)

    res = {
        'unread_message_count': _session.user.notifications.read().count(),
        'unread_selection_count': Selection_Entity.objects.get_user_unread(session=_session.session_key),
    }
    return SuccessJsonResponse(res)


def visit_item(request, item_id):
    _ttid = request.GET.get("ttid", None)
    _sid = request.GET.get("sid", None)
    _entry = request.GET.get("entry", "mobile")
    _outer_code = request.GET.get("outer_code", None)
    _sche = request.GET.get("sche", None)

    b = Buy_Link.objects.get(origin_id=item_id)

    if "taobao.com" in b.origin_source:
        _taobaoke_info = taobaoke_mobile_item_convert(b.origin_id)
        if _taobaoke_info and _taobaoke_info.has_key('click_url'):
            return HttpResponseRedirect(decorate_taobao_url(_taobaoke_info['click_url'], _ttid, _sid, _outer_code, _sche))
        return HttpResponseRedirect(decorate_taobao_url(get_taobao_url(b.origin_id, True), _ttid, _sid, _outer_code, _sche))
    else:
        return HttpResponseRedirect(b.link)
__author__ = 'edison7500'
