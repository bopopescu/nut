from django.http import HttpResponseRedirect

from apps.mobile.lib.sign import check_sign
from apps.core.utils.http import SuccessJsonResponse
from apps.core.models import Show_Banner, Banner, Buy_Link, Entity
from apps.core.utils.taobaoapi.utils import taobaoke_mobile_item_convert
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger

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

    res['config'] = {}
    res['config']['taobao_ban_count'] = 2
    res['config']['url_ban_list'] = ['http://m.taobao.com/go/act/mobile/cloud-jump.html']

    return SuccessJsonResponse(data=res)


@check_sign
def selection(request):

    _timestamp = request.GET.get('timestamp', None)

    entities = Entity.objects.selection()[0:30]
    res = list()

    for e in entities:
        r = {
            'entity':e.v3_toDict(),
            'note':e.top_note.v3_toDict(),
        }

        res.append({
            'content':r,
            'type': "note_selection",
        })

    # paginator = ExtentPaginator(entity_list)


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
