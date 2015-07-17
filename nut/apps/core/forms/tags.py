from django import forms
from django.utils.translation import gettext_lazy as _
from hashlib import md5

class TagForms(forms.Form):

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )


class EditTagForms(TagForms):

    def __init__(self, tag, *args, **kwargs):
        self.tag_cache = tag
        super(EditTagForms, self).__init__(*args, **kwargs)

    def save(self):
        _title = self.cleaned_data.get('title')
        # print _title
        self.tag_cache.name = _title
        self.tag_cache.hash = md5(_title.encode('utf-8')).hexdigest()
        return self.tag_cache.save()

__author__ = 'edison'
