from django import forms
# from django.utils.translation import gettext_lazy as _

from apps.wechat.models import Robots


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Robots
        fields = ['accept', 'type', 'content']
        widgets = {
            'accept': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


