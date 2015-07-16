from django.views.generic import ListView
from django.http import Http404
from apps.tag.models import Tags, Content_Tags
from apps.core.extend.paginator import ExtentPaginator

from django.utils.log import getLogger

log = getLogger('django')


class TagListView(ListView):
    queryset = Tags.objects.all()
    http_method_names = ['get']
    template_name = 'tag/list.html'


class TagEntityView(ListView):

    http_method_names = ['get']
    template_name = 'tag/entities.html'
    paginate_by = 30
    paginator_class = ExtentPaginator

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagEntityView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        assert self.tag_name is not None
        self.tag_name = self.tag_name.lower()
        return super(TagEntityView, self).get(request, *args, **kwargs)
        # return self.render_to_response(context={})

class TagArticleView(ListView):
    http_method_names = ['get']

__author__ = 'xiejiaxin'
