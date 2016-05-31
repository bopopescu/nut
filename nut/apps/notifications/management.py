from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from braces.views import StaffuserRequiredMixin


from apps.notifications.models import DailyPush
from apps.notifications.forms import BaseDailyPushForm


class DailyPushCreateView(StaffuserRequiredMixin, CreateView):
    form_class = BaseDailyPushForm
    model = DailyPush
    template_name = 'management/notifications/daily_push_create.html'


class DailyPushUpdateView(StaffuserRequiredMixin, UpdateView):
    pass

class DailyPushListView(StaffuserRequiredMixin, ListView):
    template_name = 'management/notifications/daily_push_list.html'

