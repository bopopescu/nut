from apps.mobile.models import LaunchBoard
from django import forms


class LaunchBoardForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )

    launchImage = forms.FileField(widget=forms.FileInput())
    title = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput())
    action = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(
        label=_('enable'),
        choices=YES_OR_NO,
        widget=forms.TextInput( attrs={'class':'form-control'}, ),
        required=False,
        help_text=_(''),
        initial=0,
    )


    def save(self):
        pass



__author__ = 'edison7500'
