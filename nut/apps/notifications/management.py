from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from braces.views import StaffuserRequiredMixin


from apps.notifications.models import DailyPush
from apps.notifications.forms
