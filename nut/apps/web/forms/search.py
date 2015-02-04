from django import forms
from django.utils.translation import gettext_lazy as _
# from haystack.forms import SearchForm
from django.utils.log import getLogger
from apps.core.models import GKUser, Entity, Tag, Entity_Tag

#
log = getLogger('django')


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search'}))

    t = forms.CharField(required=False, label=_('type'),
                        widget=forms.TextInput())

    def search(self):
        _keyword = self.get_keyword()
        _type = self.cleaned_data.get('t')
        if _type == "t":
            self.res = Tag.search.query(_keyword)
            tag_id_list = list()
            for row in self.res.all():
                log.info(row.id)
                tag_id_list.append(row.id)
            log.info(tag_id_list)
            res = Entity_Tag.objects.tags(tag_id_list)
            # print res.query
            return res

        elif _type == "u":
            self.res = GKUser.search.query(_keyword).order_by('@weight', '-date_joined')
        else:
            self.res = Entity.search.query(_keyword).order_by('@weight', '-created_time')
        return self.res


    def get_keyword(self):
        self.keyword = self.cleaned_data.get('q')

        return self.keyword

    def get_entity_count(self):
        res = Entity.search.query(self.keyword)
        return res.count()

    def get_user_count(self):
        res = GKUser.search.query(self.keyword)
        return res.count()

    def get_tag_count(self):
        res = Tag.search.query(self.keyword)
        return res.count()

__author__ = 'edison'
