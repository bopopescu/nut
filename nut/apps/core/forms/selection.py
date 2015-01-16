from django import forms
from django.utils.translation import gettext_lazy as _


class SelectionForm(forms.Form):
    pub_time = forms.DateTimeField(
        label=_('publish datetime'),
        widget=forms.DateTimeInput(attrs={'class':'form-control'}),
        help_text=_('')
    )


    def __init__(self, selection, *args, **kwargs):
        self.selection = selection
        super(SelectionForm, self).__init__(*args, **kwargs)

    def update(self):
        pass


__author__ = 'edison7500'
