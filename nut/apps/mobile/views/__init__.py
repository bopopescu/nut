from django.http import HttpResponseRedirect

from apps.mobile.lib.sign import check_sign
from apps.mobile.models import Session_Key
from apps.core.utils.http import SuccessJsonResponse, ErrorJsonResponse
from apps.core.models import Show_Banner, Banner, Buy_Link, Selection_Entity, Entity, Entity_Like, Sub_Category
from apps.core.utils.taobaoapi.utils import taobaoke_mobile_item_convert
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from datetime import datetime


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

    innqs = Show_Banner.objects.all().values_list('banner_id', flat=True)
    log.info(innqs)
    banners = Banner.objects.filter(id__in=innqs)

    res['banner'] = []
    for banner in banners:
        res['banner'].append(
            {
                'url':banner.url,
                'img':banner.image_url
            }
        )

    res['discover'] = []
    from django.db.models import Count
    el = Entity_Like.objects.popular()
    category = Entity.objects.filter(pk__in=list(el)).annotate(dcount=Count('category')).values_list('category_id', flat=True)
    for c in Sub_Category.objects.filter(pk__in=category, status=True):
        res['discover'].append(
            c.v3_toDict()
        )
    # log.info(res['discover'])


    res['config'] = {}
    res['config']['taobao_ban_count'] = 2
    res['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']

    return SuccessJsonResponse(data=res)


@check_sign
def selection(request):

    # _timestamp = request.GET.get('timestamp', None)
    _timestamp = request.GET.get('timestamp', datetime.now())
    if _timestamp != None:
        _timestamp = datetime.fromtimestamp(float(_timestamp))
    _key = request.GET.get('session')


    selections = Selection_Entity.objects.published().filter(pub_time__lte=_timestamp)[:30]
    # log.info(selections.query)

    ids = selections.values_list('entity_id', flat=True)
    # log.info("count %s" % len(ids))
    try:
        _session = Session_Key.objects.get(session_key=_key)
        # log.info("session %s" % _session)
        el = Entity_Like.objects.user_like_list(user=_session.user, entity_list=list(ids))
    except Session_Key.DoesNotExist, e:
        log.info(e.message)
        el = []
    # log.info(el)
    res = list()

    for selection in selections:
        # log.info(selection.entity_id)
        # if selection.entity_id in el:
        #     log.info("like like like ")
        r = {
            'entity':selection.entity.v3_toDict(user_like_list=el),
            'note':selection.entity.top_note.v3_toDict(),
        }

        res.append({
            'content': r,
            'post_time': selection.entity.top_note.post_timestamp,
            'type': "note_selection",
        })

    # paginator = ExtentPaginator(entity_list)
    return SuccessJsonResponse(res)

@check_sign
def popular(request):

    _scale = request.GET.get('scale', 'daily')

    popular = Entity_Like.objects.popular()
    _entities = Entity.objects.filter(id__in=list(popular))

    res = dict()
    res['content'] = list()
    res['scale'] = _scale
    for e in _entities:
        r = {
            'entity': e.v3_toDict()
        }
        res['content'].append(r)

    return SuccessJsonResponse(res)


@check_sign
def unread(request):

    res = {
        'unread_message_count': 0,
        'unread_selection_count':0,
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
