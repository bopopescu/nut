from django import forms
from django.utils.translation import ugettext_lazy as _
from apps.core.models import Category, Sub_Category
from apps.core.forms import get_category_choices


YES_OR_NO = (
    (1, _('yes')),
    (0, _('no')),
)


class CategoryForm(forms.Form):

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
        _status = self.cleaned_data.get('status')
        _status = int(_status)




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



class SubCategoryForm(forms.Form):
    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )

    category = forms.ChoiceField(
        label=_('parent category'),
        choices=get_category_choices(),
        widget=forms.Select(attrs={'class':'form-control'})
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
    )


class EditSubCategoryForm(SubCategoryForm):

    def __init__(self, sub_category, *args, **kwargs):
        self.sub_category = sub_category
        super(EditSubCategoryForm, self).__init__(*args, **kwargs)


    def save(self):
        _title = self.cleaned_data.get('title')
        _category = self.cleaned_data.get('category')
        _status = self.cleaned_data.get('status')
        _status = int(_status)

        self.sub_category.title = _title
        self.sub_category.group_id = _category
        self.sub_category.status = _status
        self.sub_category.save()



__author__ = 'edison'
