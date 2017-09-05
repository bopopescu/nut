from django import forms
from apps.wechat.models import RobotDic


class ReplyForm(forms.ModelForm):
    class Meta:
        model = RobotDic
        fields = ['keyword', 'resp', 'status']
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'resp': forms.Textarea(attrs={'class': 'form-control'}),
        }
