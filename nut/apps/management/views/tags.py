from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.forms.tags import EditTagForms
from apps.core.extend.paginator import ExtentPaginator


from django.views.generic import ListView, FormView
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


class EditTagFormView(LoginRequiredMixin, FormView):
    template_name = 'management/tags/edit.html'
    form_class = EditTagForms


    def get_success_url(self):
        # print self.tag_id
        self.success_url = reverse('management_tag_edit', args=[self.tag_id])
        return self.success_url

    def get_initial(self):
        res = super(EditTagFormView, self).get_initial()
        res.update(
            {
                'title': self.tag.name
            }
        )
        return res

    def get_form_kwargs(self):
        kwargs = super(EditTagFormView, self).get_form_kwargs()
        kwargs.update(
            {
                'tag':self.tag,
                # 'title': self.tag.name
            }
        )
        print kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        context = kwargs.copy()
        context.update(
            {
                'button': _('update'),
            }
        )
        return context

    def form_valid(self, form):
        # print form
        self.object = form.save()
        return super(EditTagFormView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.tag_id = kwargs.pop('tag_id', None)
        assert self.tag_id is not None
        try:
            self.tag = Tags.objects.get(pk = self.tag_id)
        except Tags.DoesNotExist:
            raise Http404

        return super(EditTagFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.tag_id = kwargs.pop('tag_id', None)
        assert self.tag_id is not None
        try:
            self.tag = Tags.objects.get(pk = self.tag_id)
        except Tags.DoesNotExist:
            raise Http404
        # print request.POST
        return super(EditTagFormView, self).post(request, *args, **kwargs)


__author__ = 'edison'
