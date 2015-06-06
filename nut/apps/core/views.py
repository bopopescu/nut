from django.views.generic.base import View, TemplateResponseMixin, ContextMixin


class BaseListView(TemplateResponseMixin, ContextMixin, View):

    queryset = None

    def get_queryset(self):
        return self.queryset



class BaseEditView(TemplateResponseMixin, ContextMixin, View):
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


__author__ = 'edison'
