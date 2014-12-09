from haystack.views import SearchView
from apps.web.forms.search import EntitySearchForm

class EntitySearchView(SearchView):

    template = 'web/main/search.html'
    form = EntitySearchForm

    def extra_context(self):
        extra = super(EntitySearchView, self).extra_context()

        if self.request == []:
            extra['facets'] = self.form.search().facet_counts()

        else:
            extra['facets'] = self.results.facet_counts()

        return extra

__author__ = 'edison'
