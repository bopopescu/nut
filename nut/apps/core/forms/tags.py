#coding: utf-8
from apps.core.utils.image import HandleImage
from django import forms
from django.utils.translation import gettext_lazy as _
from hashlib import md5

class TagForms(forms.Form):

    name = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )



class EditTagForms(TagForms):
    image = forms.ImageField(
        label=_('image'),
        widget=forms.FileInput(),
        required=False
    )
    description = forms.CharField(
        label=_('description'),
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, tag, *args, **kwargs):
        self.tag_cache = tag
        # self.image = tag.image
        # self.name = tag.name
        # self.description = tag.description
        super(EditTagForms, self).__init__(*args, **kwargs)


    def save(self):
        _title = self.cleaned_data.get('name')
        _description = self.cleaned_data.get('description')
        if 'image' in self.changed_data:
            new_image = self.cleaned_data.get('image')
            _image = HandleImage(new_image)
            filename = _image.save()
            self.tag_cache.image = filename
        # print _title
        self.tag_cache.name = _title
        self.tag_cache.hash = md5(_title.encode('utf-8')).hexdigest()
        self.tag_cache.description = _description

        return self.tag_cache.save()

__author__ = 'edison'
