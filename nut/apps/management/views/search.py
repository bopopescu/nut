from apps.core.models import GKUser, Entity, Article, Sub_Category
from apps.tag.models import Tags
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.views import LoginRequiredMixin, BaseJsonView
# from apps.management.forms.search import ManagementSearchForm
from apps.core.forms.search import GKSearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from django.utils.log import getLogger

log = getLogger('django')


class ManageSearchView(LoginRequiredMixin, SearchView):

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
            res = self.queryset.models(Article).order_by('-read_count')
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



class AutoCompleteView(LoginRequiredMixin, BaseJsonView):

    def get_data(self, context):
        type = self.request.GET.get('t', None)
        if type == 'c':
            sqs= SearchQuerySet().models(Sub_Category).autocomplete(title_auto=self.request.GET.get('q', ''))
        else:
            sqs = SearchQuerySet().models(Entity).autocomplete(title_auto=self.request.GET.get('q', ''))[:10]
        # print sqs

        suggestions = [result.title for result in sqs]
        return {
            'results':list(set(suggestions)),
        }



__author__ = 'jiaxin'