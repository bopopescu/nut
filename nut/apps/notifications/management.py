from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from braces.views import StaffuserRequiredMixin


from apps.notifications.models import DailyPush
from apps.notifications.forms import BaseDailyPushForm
from django.core.urlresolvers import reverse_lazy

class DailyPushCreateView(StaffuserRequiredMixin, CreateView):
    form_class = BaseDailyPushForm
    model = DailyPush
    template_name = 'management/notifications/daily_push_create.html'
    success_url = reverse_lazy('management_push_list')


class DailyPushUpdateView(StaffuserRequiredMixin, UpdateView):
    model = DailyPush
    form_class = BaseDailyPushForm
    template_name = 'management/notifications/daily_push_edit.html'
    success_url = reverse_lazy('management_push_list')

class DailyPushDeleteView(StaffuserRequiredMixin, DeleteView):
    model = DailyPush
    template_name = 'management/notifications/daily_push_delete.html'
    success_url = reverse_lazy('management_push_list')

class DailyPushSendTestView(StaffuserRequiredMixin, View):
    pass

class DailyPushSendProductionView(StaffuserRequiredMixin, View):
    pass

class DailyPushListView(StaffuserRequiredMixin, ListView):
    context_object_name = 'push_list'
    template_name = 'management/notifications/daily_push_list.html'
    def get_queryset(self):
        return DailyPush.object.all()


