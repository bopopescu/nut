from django import forms
from django.utils.translation import ugettext_lazy as _


class CommentForm(forms.Form):
    content = forms.CharField(
        label=_('content'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_(''),
    )

    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        print self.note
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):

        return


__author__ = 'edison7500'
