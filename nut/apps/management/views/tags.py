# encoding: utf-8
from apps.management.forms.tag import  SwitchTopArticleTagForm, SwitchPublishedEntityTagForm
from django.conf import settings
from django.shortcuts import  get_object_or_404, render_to_response
from braces.views import CsrfExemptMixin,UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from apps.core.forms.tags import EditTagForms
from apps.core.extend.paginator import ExtentPaginator


from django.views.generic import View,ListView, FormView, DetailView,UpdateView
from django.views.generic.detail import SingleObjectMixin
from apps.core.views import LoginRequiredMixin
from apps.tag.models import Tags, Content_Tags


from apps.core.mixins.views import SortMixin, FilterMixin
from braces.views import AjaxResponseMixin,JSONResponseMixin

from urllib import  unquote

image_host = getattr(settings, 'IMAGE_HOST', None)

class TagListView(LoginRequiredMixin,SortMixin,FilterMixin,  ListView ):
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
        elif sort_by == 'topArticleTag':
            qs = qs.filter(content_tags__target_content_type_id=31).annotate(acount=Count('content_tags')).order_by('-isTopArticleTag', '-acount')
        elif sort_by == 'publishedEntityTag':
            qs = qs.filter(content_tags__target_content_type_id=24).annotate(acount=Count('content_tags')).order_by(
                '-isPubishedEntityTag', '-acount')
        else :
            pass
        return qs

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'tag_name':
            qs = qs.filter(name__icontains=filter_value.strip())
        return qs

    # def get_queryset(self):
    #     qs = super(TagListView, self).get_queryset()
    #     return qs

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
        try:
            assert unquote(self.tag_name) == self.tag_name
        except:
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
        try :
            self.tag_name = unquote(str(self.tag_name)).decode('utf-8')
        except UnicodeEncodeError:
            pass

        assert self.tag_name is not None
        return super(ArticleTagListView, self).get(request, *args, **kwargs)


# class EditTagFormView(LoginRequiredMixin, FormView):
def EditTagFormView(request, tag_id):
    template = 'management/tags/edit.html'
    try:
        tag = Tags.objects.get(pk = tag_id)
    except Tags.DoesNotExist:
            raise Http404
    if request.method == 'POST':
        form=EditTagForms(tag, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('management_tag_list'))
    form = EditTagForms(tag, initial={'name': tag.name, 'description': tag.description})
    return render_to_response(
            template,
            {'form': form,
             'tag': tag,
             'image_host': image_host,
             'button': _('update'),
             },
            context_instance=RequestContext(request),
        )


    # def get_success_url(self):
    #     # print self.tag_id
    #     self.success_url = reverse('management_tag_edit', args=[self.tag_id])
    #     return self.success_url
    #
    # def get_initial(self):
    #     res = super(EditTagFormView, self).get_initial()
    #     res.update(
    #         {
    #             'name': self.tag.name,
    #             'image': self.tag.image,
    #             'description': self.tag.description
    #
    #         }
    #     )
    #     return res
    #
    # def get_form_kwargs(self):
    #     kwargs = super(EditTagFormView, self).get_form_kwargs()
    #     kwargs.update(
    #         {
    #             'tag':self.tag,
    #             # 'image': kwargs['data'].get('image')
    #             # 'title': self.tag.name
    #         }
    #     )
    #     return kwargs
    #
    # def get_context_data(self, **kwargs):
    #     context = kwargs.copy()
    #     context.update(
    #         {
    #             'button': _('update'),
    #             'title': self.tag.name
    #         }
    #     )
    #     return context
    #
    # def form_valid(self, form):
    #     # print form
    #     self.object = form.save()
    #     return super(EditTagFormView, self).form_valid(form)
    #
    # # def get(self):
    # #     self.tag_id = kwargs.pop('tag_id', None)
    # #     assert self.tag_id is not None
    # #     try:
    # #         self.tag = Tags.objects.get(pk = self.tag_id)
    # #     except Tags.DoesNotExist:
    # #         raise Http404
    # #
    # #     return super(EditTagFormView, self).get(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     self.tag_id = kwargs.pop('tag_id', None)
    #     assert self.tag_id is not None
    #     try:
    #         self.tag = Tags.objects.get(pk = self.tag_id)
    #     except Tags.DoesNotExist:
    #         raise Http404
    #     return super(EditTagFormView, self).post(request, *args, **kwargs)


def tag_entity_detail(request, tag_id):
    try:
        tag = Tags.objects.get(id=tag_id)
    except Tags.DoesNotExist:
        raise Http404
    queryset = Content_Tags.objects.filter(tag=tag, target_content_type_id=24)
    # for item in queryset:
    #     item.buy_link = item.target.entity.buy_links.first()

    return render_to_response('management/tags/entity_detail.html', {'queryset': queryset, 'tag': tag,
                                                                     'request': request})


class SwitchTopArticleTagView(UserPassesTestMixin,JSONResponseMixin, UpdateView):
    form_class = SwitchTopArticleTagForm
    model = Tags
    pk_url_kwarg = 'tag_id'

    def test_func(self, user):
        return user.is_staff

    # def get_form(self, form_class):
    #     pk = self.kwargs.get(self.pk_url_kwarg, None)
    #     inst = get_object_or_404(Tags, pk)
    #     return form_class(instance=inst, **self.get_form_kwargs())


    def form_invalid(self, form):
        res = {'error':1}
        return self.render_json_response(res)

    def form_valid(self, form):
        form.save()
        res = {'error':0}
        return self.render_json_response(res)
    #
    # def get(self, **kwargs):
    #     res = {'error':1}
    #     return self.render_json_response(res)
    #
    # def post(self, request, tag_id, *args, **kwargs):
    #     theTag = get_object_or_404(Tags,tag_id)
    #     theform = SwitchTopArticleTagForm(model=theTag )
    #     res = {'error': 0  , 'isTopArticleTag': 'not knoe'}
    #     return self.render_json_response(res)
    #


class SwitchPublishedEnttityTagView(UserPassesTestMixin,JSONResponseMixin, UpdateView):
    form_class = SwitchPublishedEntityTagForm
    model = Tags
    pk_url_kwarg = 'tag_id'

    def test_func(self, user):
        return user.is_staff

    def form_invalid(self, form):
        res = {'error':1}
        return self.render_json_response(res)

    def form_valid(self, form):
        form.save()
        res = {'error':0}
        return self.render_json_response(res)


__author__ = 'edison'
