# coding=utf-8
import re
from django import forms
from django.core.exceptions import ValidationError

from apps.core.models import Entity
from apps.site_banner.models import Entity_Promotion

entity_url_re = re.compile(r'\/detail\/(.+)?\/')


class BaseEntityPromotionForm(forms.ModelForm):
    entity_url = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(BaseEntityPromotionForm,self).__init__(*args, **kwargs)

    def clean_pos(self):
        pos = self.cleaned_data.get('pos')
        return int(pos)

    def clean_entity_url(self):

        url = self.cleaned_data.get('entity_url')
        if url is None:
            raise ValidationError(u'输入果库商品URL')
        else:
            res = entity_url_re.findall(url)
            if len(res) > 0:
                self.parsed_entity_url = res[0]
                self.parsed_entity = Entity.objects.get(entity_hash=self.parsed_entity_url)
            else:
                raise ValidationError(u'输入正确果库商品URL')

        return url

    def save(self, commit=True):
        self.instance.entity = self.parsed_entity
        res = super(BaseEntityPromotionForm, self).save()
        return res

    class Meta:
        model = Entity_Promotion
        fields = ['pos', 'entity_url']


class IndexTopEntityPromotionForm(BaseEntityPromotionForm):
    def save(self):
        res = super(IndexTopEntityPromotionForm, self).save()
        self.instance.area = 'index_top'
        self.instance.save()
        return res
