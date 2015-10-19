from apps.core.models import Article, Event

from apps.api.serializers.events import EventSerializer
from rest_framework import generics
from rest_framework.permissions import  IsAdminUser


from django.shortcuts import get_object_or_404 as _get_object_or_404

from django.http import Http404
def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError):
        raise Http404

#this view is not used
class RFEventListView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    paginate_by=20

    def get_event(self):
        event_id = self.kwargs.pop('event_id', None)
        _event = get_object_or_404(Event, id=event_id)
        return _event


class RFEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Event.objects.all().order_by('created_datetime')
    serializer_class = EventSerializer


