from apps.core.views import BaseSearchView


class SearchForm(BaseSearchView):
    template_name = ''

    def get(self, request):
        form = self.get_form_class()
        if form.is_valid():
            res = form.search()
        # return self.render_to_response()


__author__ = 'jiaxin'