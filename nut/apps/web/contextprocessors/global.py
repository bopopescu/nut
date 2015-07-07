
from apps.core.models import Event
# from django.core.cache import  cache

def lastslug(request):
    "A global context processor for current event slug"

    #  TODO : add time ordering
    events = Event.objects.filter(status=True)
    slug = ''
    if len(events) > 0:
        event = events[0]
        slug = event.slug

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
        'isAndroid': ('Android' in agent_string),
    }

if __name__ == "__main__":
   print lastslug()