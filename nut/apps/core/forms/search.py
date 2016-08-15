from django import forms
from django.utils.translation import gettext_lazy as _
from haystack.forms import SearchForm as haystackSearchForm
from apps.core.models import Article, Entity, GKUser
from apps.tag.models import Tags


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    def search(self):
        pass

    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')
        return self.keyword


class GKSearchForm(haystackSearchForm):

    def search(self, type='e'):
        if 'a' ==  type:
            sqs = self.searchqueryset.filter(content=self.cleaned_data['q'], is_selection=True)
        else:
            sqs = super(GKSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()
        return sqs

    def get_article_count(self):
        return self.searchqueryset.filter(content=self.cleaned_data['q'], is_selection=True).\
            models(Article).count()

    def get_entity_count(self):
        return self.searchqueryset.filter(content=self.cleaned_data['q']).\
            models(Entity).count()

    def get_user_count(self):
        return self.searchqueryset.filter(content=self.cleaned_data['q']).\
            models(GKUser).count()

    def get_tag_count(self):
        return self.searchqueryset.filter(content=self.cleaned_data['q']).\
            models(Tags).count()


__author__ = 'edison'
