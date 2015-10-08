from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from apps.core.forms.tags import EditTagForms
from apps.core.extend.paginator import ExtentPaginator


from django.views.generic import View,ListView, FormView
from apps.core.views import LoginRequiredMixin
from apps.tag.models import Tags, Content_Tags


from apps.core.mixins.views import SortMixin
from braces.views import AjaxResponseMixin,JSONResponseMixin

from urllib import  unquote


class TagListView(LoginRequiredMixin,SortMixin, ListView ):
    default_sort_params = ('id', 'desc')
    template_name = 'management/tags/list.html'
    queryset = Tags.objects.all()
    paginate_by = 30
    paginator_class = ExtentPaginator

    def get_context_data(self, *args, **kwargs):
        context = super(TagListView, self).get_context_data()
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by='+context['sort_by']
        return context

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'article':
            qs = qs.filter(content_tags__target_content_type_id=31).annotate(acount=Count('content_tags')).order_by('-acount')
        elif sort_by ==  'entity':
            qs = qs.filter(content_tags__target_content_type_id=24).annotate(acount=Count('content_tags')).order_by('-acount')
        else :
            pass
        return qs







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
        self.queryset = Content_Tags.objects.filter(tag=self.tag, target_content_type_id=24)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(TagEntitiesView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        self.tag_name = unquote(str(self.tag_name)).decode('utf-8')
        assert self.tag_name is not None
        return super(TagEntitiesView, self).get(request, *args, **kwargs)


class ArticleTagListView(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 30
    template_name = 'management/tags/articles.html'

    def get_queryset(self):
        try:
            self.tag = Tags.objects.get(name=self.tag_name)
        except Tags.DoesNotExist:
            raise Http404
        self.queryset = Content_Tags.objects.filter(tag=self.tag, target_content_type_id=31)
        return self.queryset

    def get_context_data(self, **kwargs):
        res = super(ArticleTagListView, self).get_context_data(**kwargs)
        res.update(
            {
                'tag': self.tag,
            }
        )
        return res

    def get(self, request, *args, **kwargs):
        self.tag_name = kwargs.pop('tag_name', None)
        self.tag_name = unquote(str(self.tag_name)).decode('utf-8')
        assert self.tag_name is not None
        return super(ArticleTagListView, self).get(request, *args, **kwargs)


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
                'title': self.tag.name
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
        return super(EditTagFormView, self).post(request, *args, **kwargs)



from apps.management.forms.tag import  SwitchTopArticleTagForm

class SwitchTopArticleTagView(JSONResponseMixin, FormView):
    form_class = SwitchTopArticleTagForm
    def get_object(self):
        pass

    def form_invalid(self, form):
        res = {'id': form.cleaned_data['id'],'isTopArticleTag':form.cleaned_data}
        pass

    def form_invalid(self, form):
        pass



__author__ = 'edison'
