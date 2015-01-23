from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    t = forms.CharField(required=False, label=_('type'),
                        widget=forms.TextInput())

    def search(self):
        pass


    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')
        return self.keyword


__author__ = 'edison'
