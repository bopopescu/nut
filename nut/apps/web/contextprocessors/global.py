
from apps.core.models import Event
from django.core.cache import  cache

def lastslug(request):
    "A global context processor for current event slug"
    key = 'last_event_slug'
    slug = cache.get(key, None)
    if slug is None:
        events = Event.objects.filter(status=True)
        slug = ''
        if len(events) > 0:
            event = events[0]
            slug = event.slug
            cache.set(key, slug , timeout=6*3600)
    else:
        pass
    return {
        'newest_event_slug': slug,
    }

def browser(request):
    agent_string = request.META['HTTP_USER_AGENT']
    return {
        'isGuokuIphoneApp': 'orange' in agent_string,
        'isGuokuIpadApp': 'pomelo' in agent_string,
        'isWechat': 'MicroMessenger' in  agent_string,
        'isMobileSafari': ('iPhone' in agent_string) and ('Mobile' in agent_string) and ('Safari' in agent_string),
        'isAndroid': ('guoku-client' in agent_string),
    }

if __name__ == "__main__":
   print lastslug()