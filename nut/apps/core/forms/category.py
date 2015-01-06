from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.core.models import Category, Sub_Category


class CategoryForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
    )


class CreateCategoryForm(CategoryForm):

    def save(self):

        _title = self.cleaned_data.get('title')


class EditCategoryForm(CategoryForm):

    def __init__(self, category, *args, **kwargs):

        self.category_cache = category
        super(EditCategoryForm, self).__init__(*args, **kwargs)

    def save(self):

        _title = self.cleaned_data.get('title')
        _status = self.cleaned_data.get('status')

        _status = int(_status)
        # print _status

        self.category_cache.title = _title
        self.category_cache.status = _status
        self.category_cache.save()

        return self.category_cache




__author__ = 'edison'
