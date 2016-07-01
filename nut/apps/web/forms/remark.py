from django.forms import ModelForm, Textarea, HiddenInput, NumberInput
from apps.core.models import Article_Remark


class ArticleRemarkForm(ModelForm):
    class Meta:
        model = Article_Remark
        fields = ['content', 'reply_to']

        localized_fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
            'reply_to': HiddenInput
        }


