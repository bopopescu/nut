from apps.core.models import GKUser, Entity, Article
from apps.tag.models import Tags
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.views import LoginRequiredMixin
# from apps.management.forms.search import ManagementSearchForm
from apps.core.forms.search import GKSearchForm
from haystack.generic_views import SearchView
from django.utils.log import getLogger

log = getLogger('django')


class ManageSearchView(SearchView, LoginRequiredMixin):

    template_name = 'management/search/search.html'
    form_class = GKSearchForm
    paginator_class = ExtentPaginator

    def form_valid(self, form):
        self.queryset = form.search()
        if 'u' in self.type:
            res = self.queryset.models(GKUser).order_by('-fans_count')
        elif 't' in self.type:
            res = self.queryset.models(Tags).order_by('-note_count')
        elif 'a' in self.type:
            res = self.queryset.models(Article)
        else:
            res = self.queryset.models(Entity).order_by('-like_count')
        # log.info(res)
        context = self.get_context_data(**{
            self.form_name: form,
            'query': form.cleaned_data.get(self.search_field),
            'object_list': res,
            'type': self.type,
            'entity_count': self.queryset.models(Entity).count(),
            'user_count': self.queryset.models(GKUser).count(),
            'tag_count': self.queryset.models(Tags).count(),
            'article_count': self.queryset.models(Article).count(),
        })
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.type = request.GET.get('t', 'e')
        return super(ManageSearchView, self).get(request, *args, **kwargs)

# class SearchForm(BaseSearchView):
#     template_name = 'management/search/search.html'
#     form_class = ManagementSearchForm
#
#     def get(self, request):
#         _page = request.GET.get('page', 1)
#         form = self.get_form_class()
#         if form.is_valid():
#             res = form.search()
#             paginator = ExtentPaginator(res, 24)
#             try:
#                 _objects = paginator.page(_page)
#             except PageNotAnInteger:
#                 _objects = paginator.page(1)
#             except EmptyPage:
#                 raise Http404
#
#             log.info("count %s" % form.get_type())
#
#             context = {
#                 'objects' : _objects,
#                 'keyword': form.get_keyword(),
#                 'type': form.get_type(),
#             }
#             return self.render_to_response(context)


__author__ = 'jiaxin'