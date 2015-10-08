from django.forms import ModelForm
from django import forms

from apps.tag.models import Tags
class SwitchTopArticleTagForm(ModelForm):

    isTopArticleTag = forms.BooleanField()
    class Meta:
        model = Tags
        fields = ['id', 'isTopArticleTag']