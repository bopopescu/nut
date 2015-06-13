from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.contrib.auth.decorators import login_required
from apps.core.forms.search import SearchForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class BaseListView(LoginRequiredMixin, TemplateResponseMixin, ContextMixin, View):

    queryset = None

    def get_queryset(self):
        return self.queryset


class BaseFormView(TemplateResponseMixin, ContextMixin, View):
    initial = {}
    form_class = None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form_class(self):

        return self.form_class(**self.get_form_kwargs())


class BaseSearchView(BaseFormView):

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
        }

        if self.request.method in ('GET'):
            kwargs.update({
                'data': self.request.GET,
                # 'files': self.request.FILES,
            })
        return kwargs


__author__ = 'edison'
