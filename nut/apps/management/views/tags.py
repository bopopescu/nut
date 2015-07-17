from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import gettext_lazy as _

from apps.core.models import Tag, Entity_Tag
from apps.core.forms.tags import EditTagForms
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage


from django.views.generic import ListView
from apps.core.views import LoginRequiredMixin
from apps.tag.models import Tags, Content_Tags


class TagListView(LoginRequiredMixin, ListView):
    template_name = 'management/tags/list.html'
    queryset = Tags.objects.all()
    paginate_by = 30
    paginator_class = ExtentPaginator


class TagEntitiesView(LoginRequiredMixin, ListView):

    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 30
    template_name = 'management/tags/entities.html'

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagEntitiesView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        print res
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        assert self.tag_name is not None
        return super(TagEntitiesView, self).get(request, *args, **kwargs)


# def list(request, template='management/tags/list.html'):
#
#     page = request.GET.get('page', 1)
#     tag_list = Tag.objects.all()
#
#     paginator = ExtentPaginator(tag_list, 30)
#     try:
#         _tags = paginator.page(page)
#     except InvalidPage:
#         _tags = paginator.page(1)
#     except EmptyPage:
#         raise Http404
#
#     return render_to_response(
#             template,
#             {
#                 'tags': _tags,
#             },
#             context_instance = RequestContext(request)
#         )


def edit(request, tag_id, template='management/tags/edit.html'):

    try:
        _tag = Tag.objects.get(pk = tag_id)
    except Tag.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EditTagForms(_tag, request.POST)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EditTagForms(_tag, initial={
            'title':_tag.tag,
        })


    return render_to_response(
        template,
        {
            'forms': _forms,
            'button': _('update'),
        },
        context_instance = RequestContext(request)
    )


def entities(request, tag_id, templates="management/tags/entities.html"):


    return render_to_response(
        templates,
        {

        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison'
