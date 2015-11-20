from django.views.generic import FormView, ListView
from apps.mobile.models import LaunchBoard
from apps.mobile.forms import LaunchBoardForm, CreateLaunchBoardForm
# from django.core.urlresolvers import reverse


class LaunchBoardListView(ListView):
    model = LaunchBoard
    template_name = "management/marketing/list.html"


class NewLaunchBoardView(FormView):
    form_class = CreateLaunchBoardForm
    template_name = "management/marketing/create.html"
    success_url = "/management/marketing/"

    def form_valid(self, form):
        form.save()
        return super(NewLaunchBoardView, self).form_valid(form)


class EditLaunchBoardView(FormView):
    form_class = LaunchBoardForm
    template_name = "management/marketing/edit.html"
