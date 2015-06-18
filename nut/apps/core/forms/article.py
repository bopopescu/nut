from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.log import getLogger
from django.core.exceptions import ObjectDoesNotExist

from apps.core.models import Article, Selection_Article
from apps.core.utils.image import HandleImage
from datetime import datetime



log = getLogger('django')

class BaseSelectionArticleForm(forms.Form):
    article_id = forms.CharField(required=False)
    is_published = forms.BooleanField(required=False)
    pub_time = forms.DateTimeField(required=False)

    def get_article_obj(self):
        return Article.objects.get(pk=self.cleaned_data['article_id'])

    def clean_article(self):
        article_id = self.cleaned_data['article_id']
        try :
            the_article = Article.objects.get(pk=article_id, publish=Article.published)
        except Article.DoesNotExist:
            raise forms.ValidationError(_('can not find article'),
                                         code='invalid_article_id ')
        return article_id

    def save(self):
        _the_article = self.get_article_obj()
        _is_published = self.cleaned_data.get('is_published', False)
        _pub_time = self.cleaned_data.get('pub_time', None)

        selection_article = Selection_Article(is_published=_is_published, pub_time=_pub_time)
        selection_article.article = _the_article
        try :
            selection_article.save()
        except Exception as e :
            log(e)
        return selection_article.id



class CreateSelectionArticleForm(BaseSelectionArticleForm):
    pass

class EditSelectionArticleForm(BaseSelectionArticleForm):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    article_id = forms.CharField(
            widget=forms.TextInput(attrs={'class':'form-control', 'disabled':''}),
            required=False,
        )
    is_published = forms.ChoiceField(
        label=_('is_published'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
        help_text=_(''),
        initial=1,
    )

    pub_time = forms.DateTimeField(
        label=_('publish datetime'),
        widget=forms.DateTimeInput(attrs={'class':'form-control'}),
        help_text=_(''),
        initial=datetime.now()
    )

    def __init__(self, sla, *args, **kwargs):
        self.sla = sla
        super(EditSelectionArticleForm, self).__init__(*args, **kwargs)


class RemoveSelectionArticleForm(BaseSelectionArticleForm):
    pass




class BaseArticleForms(forms.Form):
    cover = forms.CharField(
        label = _('cover'),
        widget=forms.TextInput(attrs={'class':'cover-input'}),
        required=False,
    )

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

    # cover = forms.ImageField(
    #     label=_('cover'),
    #     widget=forms.FileInput(),
    #     required=False,
    # )

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
        article.cover = _cover
        #  use stand along method to handle cover image
        # if _cover:
        #     log.info(_cover)
        #     _image = HandleImage(_cover)
        #     article.cover = _image.save()

        article.save()

        return article




class EditArticleForms(BaseArticleForms):

    def __init__(self, article, *args, **kwargs):
        self.article = article
        super(EditArticleForms, self).__init__(*args, **kwargs)
        if self.article.is_published:
            self.fields['is_publish'] = forms.ChoiceField(
            label=_('publish'),
            choices=Article.ARTICLE_STATUS_CHOICES,
            widget=forms.Select(attrs={'class':'form-control', 'disabled':''}),
            required=False,
            # help_text=_(''),
            # initial=Article.draft,
        )


    def save(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')


        self.article.title = title
        self.article.content = content

        if not self.article.is_published:
            is_publish = self.cleaned_data.get('is_publish')
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
