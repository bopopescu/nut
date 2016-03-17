from django.views.generic.base import View, TemplateResponseMixin, ContextMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apps.core.utils.http import JSONResponse, ErrorJsonResponse


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        if context:
            return JSONResponse(
                self.get_data(context),
                **response_kwargs
            )
        return ErrorJsonResponse(status=404)

    def get_data(self, context):
        return context


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class BaseListView(LoginRequiredMixin, TemplateResponseMixin, ContextMixin,
                   View):
    queryset = None

    def get_queryset(self):
        return self.queryset


class BaseJsonView(JSONResponseMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


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
    # form_class = SearchForm

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

    def get_form_class(self):
        return self.form_class(**self.get_form_kwargs())


__author__ = 'edison'
