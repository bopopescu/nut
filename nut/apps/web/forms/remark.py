from django.forms import ModelForm, Textarea
from apps.core.models import Article_Remark


class ArticleRemarkForm(ModelForm):
    class Meta:
        model = Article_Remark
        fields = ['content']
        localized_fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 6}),
        }

