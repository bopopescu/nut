from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger


from apps.core.models import Article

log = getLogger('django')


class BaseArticleForms(forms.Form):

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text = _(''),
    )

    content = forms.CharField(
        label=_('content'),
        widget=forms.Textarea(attrs={'class':'form-control', 'id':'summernote'}),
        help_text=_(''),
    )

    is_publish = forms.ChoiceField(
        label=_('publish'),
        choices=Article.ARTICLE_STATUS_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    def cleaned_is_publish(self):
        _is_publish = self.cleaned_data.get('is_publish')
        return int(_is_publish)


class CreateArticleForms(BaseArticleForms):


    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(CreateArticleForms, self).__init__(*args, **kwargs)


    def save(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')

        article = Article(
            title = title,
            content = content,
        )
        article.creator = self.user_cache
        article.save()

        return article



class EditArticleForms(BaseArticleForms):


    def __init__(self, article, *args, **kwargs):
        self.article = article
        super(EditArticleForms, self).__init__(*args, **kwargs)


    def save(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        is_publish = self.cleaned_data.get('is_publish')


        self.article.title = title
        self.article.content = content
        self.article.publish = is_publish
        self.article.save()

        return self.article



__author__ = 'edison'
