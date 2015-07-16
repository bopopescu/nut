from django.views.generic import ListView, DetailView
from apps.tag.models import Tags, Content_Tags


class TagListView(ListView):
    queryset = Tags.objects.all()
    http_method_names = ['get']


class TagEntityView(ListView):

    http_method_names = ['get']
    template_name = 'tag/entities.html'

    def get(self, tag_name, **kwargs):


        return self.render_to_response(context={})

__author__ = 'xiejiaxin'
