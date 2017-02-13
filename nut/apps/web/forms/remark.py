import bleach
from django.forms import ModelForm, Textarea, HiddenInput, NumberInput
from apps.core.models import Article_Remark


ALLOWED_REMARK_TAGS=[]

class ArticleRemarkForm(ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get('content')
        return bleach.clean(content, tags=ALLOWED_REMARK_TAGS)


    class Meta:
        model = Article_Remark
        fields = ['content', 'reply_to']

        localized_fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 3}),
            'reply_to': HiddenInput
        }


