# coding=utf-8

from django.views.generic import ListView
from apps.core.models import Friendly_Link


class FriendlyLinkListView(ListView):
    template_name = 'web/links.html'
    context_object_name = 'flinks'

    def get_queryset(self):
        return Friendly_Link.objects.all()

