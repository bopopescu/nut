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
    return {
        'newest_event_slug': slug,
    }


def browser(request):
    static_url = settings.STATIC_URL

    if request.is_secure():
        static_url = static_url.replace('http://', 'https://')

    try:
        agent_string = request.META['HTTP_USER_AGENT']
    except KeyError:
        agent_string = ''
    return {
        'isGuokuIphoneApp': 'orange' in agent_string,
        'isGuokuIpadApp': 'pomelo' in agent_string,
        'isWechat': 'MicroMessenger' in agent_string,
        'isMobileSafari': ('iPhone' in agent_string) and ('Mobile' in agent_string) and ('Safari' in agent_string),
        'isAndroid': ('guoku-client' in agent_string),
        'global_static_url_prefix': static_url,
        'is_secure': request.is_secure()
    }


def is_from_mobile(request):
    if hasattr(settings, 'ANT_SIMULATE_MOBILE') and settings.ANT_SIMULATE_MOBILE:
        res = True
    else:
        try:
            host_str = request.META['HTTP_HOST']
        except KeyError:
            host_str = ''

        res = 'm.guoku.com' in host_str

    return {'isFromMobile': res}
