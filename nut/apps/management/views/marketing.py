from django.http import Http404
from django.views.generic import FormView, ListView
from apps.mobile.models import LaunchBoard
from apps.mobile.forms import LaunchBoardForm, CreateLaunchBoardForm, EditLaunchBoardForm
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
    form_class = EditLaunchBoardForm
    template_name = "management/marketing/edit.html"

    def get_object(self):
        try:
            obj = LaunchBoard.objects.get(pk = self.lid)
        except LaunchBoard.DoesNotExist:
            raise Http404
        return obj

    # def get_form_kwargs(self):
    #
    #
    #     return

    def get_initial(self):
        initial = super(EditLaunchBoardView, self).get_initial()
        initial.update(
            {
                "title": self.object.title,
                "description": self.object.description,
                "action": self.object.action,
                "status": self.object.status,
            }
        )
        return initial

    def get_context_data(self, **kwargs):
        kwargs.update(
            {
                "object": self.object
            }
        )
        return kwargs

    def get(self, request, *args, **kwargs):
        self.lid = kwargs.pop('lid', None)
        assert self.lid is not None
        self.object = self.get_object()

        return super(EditLaunchBoardView, self).get(request, *args, **kwargs)
