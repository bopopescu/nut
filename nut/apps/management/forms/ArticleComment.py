# coding=utf-8

from django.forms import ModelForm
from apps.core.models import Article_Remark


class ArticleCommentForm(ModelForm):
    class Meta:
        model = Article_Remark
        fields = ['content']
