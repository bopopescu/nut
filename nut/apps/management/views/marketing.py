from django.views.generic import FormView, ListView
from apps.mobile.models import LaunchBoard


class LaunchBoardListView(ListView):
    model = LaunchBoard
    template_name = "management/marketing/list.html"