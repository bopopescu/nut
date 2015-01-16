from django import forms
from django.utils.translation import gettext_lazy as _


class SelectionForm(forms.Form):
    YES_OR_NO = (
        (1, _('yes')),
        (0, _('no')),
    )

    pub_time = forms.DateTimeField(
        label=_('publish datetime'),
        widget=forms.DateTimeInput(attrs={'class':'form-control'}),
        help_text=_('')
    )

    is_published = forms.ChoiceField(
        label=_('is_published'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
        help_text=_(''),
        initial=1,
    )

    def __init__(self, selection, *args, **kwargs):
        self.selection = selection
        super(SelectionForm, self).__init__(*args, **kwargs)

    def update(self):
        _pub_time = self.cleaned_data.get('pub_time')
        _is_published = self.cleaned_data.get('is_published')

        _is_published = int(_is_published)

        self.selection.pub_time = _pub_time
        self.selection.is_published = _is_published
        self.selection.save()

        return self.selection


__author__ = 'edison7500'
