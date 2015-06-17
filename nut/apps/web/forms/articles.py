from django.forms import forms, ModelForm

from apps.core.forms.article import BaseArticleForms
from apps.core.models import Article

class WebArticleEditForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'cover', 'content','publish']

