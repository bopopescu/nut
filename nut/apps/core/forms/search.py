from django import forms
from django.utils.translation import gettext_lazy as _
from haystack.forms import SearchForm as haystackSearchForm
# from apps.core.models import Entity

class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    t = forms.CharField(required=False, label=_('type'),
                        widget=forms.TextInput(),
                        initial='e')

    def search(self):
        pass

    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')
        return self.keyword


class GKSearchForm(haystackSearchForm):

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(GKSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()
        return sqs

__author__ = 'edison'
