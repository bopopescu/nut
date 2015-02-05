from django import forms
# from django.utils.translation import gettext_lazy as _
from apps.wechat.models import Robots


class RobotsForm(forms.ModelForm):

    class Meta:
        model = Robots
        widgets = {
            'accept': forms.TextInput(attrs={'class':'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            # 'content': forms.Textarea(attrs={'class':'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(RobotsForm, self).__init__(*args, **kwargs)

__author__ = 'edison7500'
