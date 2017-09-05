from django.forms import ModelForm
from django import forms
from apps.wechat.models import RobotDic


class BaseKeywordForm(ModelForm):
    resp = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = RobotDic
