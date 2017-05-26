# coding=utf-8
from apps.core.models import Event
from django.core.cache import cache

from django.conf import settings


def last_slug(request):
    """A global context processor for current event slug
    :type request: object
    """
    key = 'last_event_slug'
    slug = cache.get(key, None)
    if slug is None:
        events = Event.objects.filter(status=True)
        slug = ''
        if len(events) > 0:
            event = events[0]
            slug = event.slug
            cache.set(key, slug, timeout=6 * 3600)
    else:
        pass
    return {'newest_event_slug': slug}


def browser(request):
    """
    获取浏览器相关信息
    """
    static_url = settings.STATIC_URL.replace('http://', 'https://') if request.is_secure() else settings.STATIC_URL

    ua = request.META.get('HTTP_USER_AGENT', '').lower()

    return {
        'isGuokuIphoneApp': 'orange' in ua,
        'isGuokuIpadApp': 'pomelo' in ua,
        'isWechat': 'micromessenger' in ua,
        'isMobileSafari': ('iphone' in ua) and ('mobile' in ua) and ('safari' in ua),
        'isAndroid': 'guoku-client' in ua,
        'isBaiduApp': 'baiduboxapp' in ua or 'dev.guoku.com' in request.META.get('HTTP_HOST', ''),
        'global_static_url_prefix': static_url,
        'is_secure': request.is_secure()
    }


def check_is_from_mobile(request):
    """
    判断请求是否来自于果库手机app
    # TODO: 完善判断依据，从host改为user agent
    """
    if getattr(settings, 'ANT_SIMULATE_MOBILE', False):
        is_from_mobile = True
    else:
        is_from_mobile = 'm.guoku.com' in request.META.get('HTTP_HOST', '')

    return {'isFromMobile': is_from_mobile}
