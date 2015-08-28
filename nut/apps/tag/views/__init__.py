from django.views.generic import ListView
from django.http import Http404
from apps.tag.models import Tags, Content_Tags
from apps.core.extend.paginator import ExtentPaginator
from apps.core.models import Entity_Like, Note
from django.utils.log import getLogger

log = getLogger('django')


class TagListView(ListView):
    queryset = Tags.objects.all()
    http_method_names = ['get']
    template_name = 'tag/list.html'


class TagEntityView(ListView):

    http_method_names = ['get']
    template_name = 'tag/entities.html'
    paginate_by = 20
    paginator_class = ExtentPaginator

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag, target_content_type_id=24)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagEntityView, self).get_context_data(**kwargs)
        contenttag_list = res['object_list']

        if self.request.user.is_authenticated():
            note_id_list = contenttag_list.values_list("target_object_id", flat=True)
            eid_list = Note.objects.filter(pk__in=list(note_id_list)).values_list('entity_id', flat=True)
            el =  Entity_Like.objects.filter(entity_id__in=list(eid_list), user=self.request.user).values_list('entity_id', flat=True)

        res.update(
            {
                'tag': self.tag,
                'user_entity_likes':el,
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
    template_name = 'tag/articles.html'
    paginate_by = 20
    paginator_class = ExtentPaginator

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name = self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag, target_content_type_id=31)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagArticleView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        assert self.tag_name is not None
        
        return super(TagArticleView, self).get(request, *args, **kwargs)


__author__ = 'xiejiaxin'
