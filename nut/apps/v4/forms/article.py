from django.forms import ModelForm, Textarea, HiddenInput
# from apps.core.models import Article_Remark
from apps.v4.models import APIArticle_Remark

class APIArticleRemarkForm(ModelForm):
    class Meta:
        model = APIArticle_Remark
        fields = ['content', 'reply_to']

        localized_fields = '__all__'
        # widgets = {
        #     'content': Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
        #     # 'reply_to': HiddenInput
        # }





__author__ = 'edison'
