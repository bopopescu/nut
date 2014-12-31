from django import forms
from django.utils.translation import gettext_lazy as _
# from haystack.forms import SearchForm
from django.utils.log import getLogger
from apps.core.models import GKUser, Entity

#
log = getLogger('django')


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    t = forms.CharField(required=False, label=_('type'),
                        widget=forms.TextInput())

    def search(self):
        _keyword = self.get_keyword()
        # _type = self.cleaned_data.get('t')
        # log.info(self.cleaned_data.get('q'))
        # log.info("OKOKOKO")
        # pass
        # _keyword = self.cleaned_data.get('q')
        sqs = list()
        # if _type == 'u':
        res = Entity.search.query(_keyword)
        sqs.append({
            'name':_('entity'),
            'type': 'e',
            'res': res,
        })

        u_res = GKUser.search.query(_keyword)
        sqs.append({
            'name': _('user'),
            'type': 'u',
            'res': u_res,
        })

        log.info(sqs)
        return sqs

    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')

        return self.keyword

    def get_search_type(self):
        # self.type = self.cleaned_data.get('t')
        self.type = self.cleaned_data.get('t')
        if self.type is None:
            self.type = 'e'

        return self.type

__author__ = 'edison'
