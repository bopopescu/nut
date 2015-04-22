
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