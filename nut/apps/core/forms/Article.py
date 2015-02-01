from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Article
from apps.core.utils.image import HandleImage


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
        initial=Article.draft,
    )

    def cleaned_is_publish(self):
        _is_publish = self.cleaned_data.get('is_publish')
        return int(_is_publish)


class CreateArticleForms(BaseArticleForms):

    cover = forms.ImageField(
        label=_('cover'),
        widget=forms.FileInput(),
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(CreateArticleForms, self).__init__(*args, **kwargs)


    def save(self):
        _title = self.cleaned_data.get('title')
        _content = self.cleaned_data.get('content')
        _is_publish = self.cleaned_data.get('is_publish')
        _cover = self.cleaned_data.get('cover')

        article = Article(
            title = _title,
            content = _content,
        )
        article.creator = self.user_cache
        article.publish = _is_publish
        if _cover:
            log.info(_cover)
            _image = HandleImage(_cover)
            article.cover = _image.save()

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


class UploadCoverForms(forms.Form):
    cover_file = forms.ImageField(
        widget=forms.FileInput()
    )

    def __init__(self, article, *args, **kwargs):
        self.article_cache = article
        super(UploadCoverForms, self).__init__(*args, **kwargs)

    def save(self):
        _cover = self.cleaned_data.get('cover_file')

        _image = HandleImage(_cover)
        filename = _image.save()
        self.article_cache.cover = filename
        self.article_cache.save()

        return self.article_cache.cover_url

__author__ = 'edison'
