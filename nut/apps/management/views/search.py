from django.http import Http404
from apps.core.views import BaseSearchView
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.management.forms.search import ManagementSearchForm
from django.utils.log import getLogger

log = getLogger('django')


class SearchForm(BaseSearchView):
    template_name = 'management/search/search.html'
    form_class = ManagementSearchForm

    def get(self, request):
        _page = request.GET.get('page', 1)
        form = self.get_form_class()
        if form.is_valid():
            res = form.search()
            paginator = ExtentPaginator(res, 24)
            try:
                _objects = paginator.page(_page)
            except PageNotAnInteger:
                _objects = paginator.page(1)
            except EmptyPage:
                raise Http404

            log.info("count %s" % form.get_type())

            context = {
                'objects' : _objects,
                'keyword': form.get_keyword(),
                'type': form.get_type(),
            }
            return self.render_to_response(context)


__author__ = 'jiaxin'