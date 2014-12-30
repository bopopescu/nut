from django import forms
from django.utils.translation import gettext_lazy as _
# from haystack.forms import SearchForm
from django.utils.log import getLogger
from apps.core.models import GKUser

#
log = getLogger('django')
#
#
# class EntitySearchForm(SearchForm):
#     start_date = forms.DateField(required=False)
#     end_date = forms.DateField(required=False)
#
#     def search(self):
#         sqs = super(EntitySearchForm, self).search()
#         if not self.is_valid():
#             return self.no_query_found()
#
#         # if self.cleaned_data['start_date']:
#         #     sqs = sqs.filter(created_time__gte=self.cleaned_data['sta'])
#
#         return sqs
#

class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    t = forms.CharField(required=False, label=_('type'),
                        widget=forms.TextInput())
    
    def search(self):
        _keyword = self.get_keyword()
        # log.info(self.cleaned_data.get('q'))
        # log.info("OKOKOKO")
        # pass
        # _keyword = self.cleaned_data.get('q')
        sqs = GKUser.search.query(_keyword)
        return sqs

    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')

        return self.keyword

__author__ = 'edison'
