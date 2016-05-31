#coding=utf-8

from django.forms import  ModelForm
from django import  forms
from apps.notifications.models import DailyPush
from django.utils.translation import ugettext_lazy as _


class BaseDailyPushForm(ModelForm):
    status = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    def __init__(self, *args, **kwargs):
        super(BaseDailyPushForm,self).__init__(*args, **kwargs)
        for key , field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
    class Meta:
        model =  DailyPush