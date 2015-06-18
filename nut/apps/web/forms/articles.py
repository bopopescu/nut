from django.forms import  ModelForm

from apps.core.models import Article


class WebArticleEditForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'cover', 'content','publish','showcover']

