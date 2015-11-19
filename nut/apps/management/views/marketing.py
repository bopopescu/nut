from django.views.generic import FormView, ListView, CreateView
from apps.mobile.models import LaunchBoard
from apps.mobile.forms import LaunchBoardForm


class LaunchBoardListView(ListView):
    model = LaunchBoard
    template_name = "management/marketing/list.html"


class NewLaunchBoardView(CreateView):
    form_class = LaunchBoardForm
    template_name = "management/marketing/create.html"


class EditLaunchBoardView(FormView):
    form_class = LaunchBoardForm
    template_name = "management/marketing/edit.html"
