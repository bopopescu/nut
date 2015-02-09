from django.views.generic.base import View, TemplateResponseMixin, ContextMixin


class DetailView(TemplateResponseMixin, ContextMixin, View):

    template_name =  ""

__author__ = 'edison'
