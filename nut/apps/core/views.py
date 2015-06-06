from django.views.generic.base import View, TemplateResponseMixin, ContextMixin


class BaseListView(TemplateResponseMixin, ContextMixin, View):

    queryset = None

    def get_queryset(self):
        return self.queryset


__author__ = 'edison'
