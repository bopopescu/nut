from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UserSignInForm(forms.Form):

    next = forms.CharField(required=False, widget=forms.HiddenInput())

    email = forms.EmailField(
        label=_('email'),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _('email')}),
        help_text=_('')
    )
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': _('password')}),
        help_text=_(''),

    )


    def __init__(self, request, *args, **kwargs):

        self.request = request
        self.user_cache = None

        super(UserSignInForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()

        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['email'].label:
            self.fields['email'].label = self.username_field.verbose_name

    # def clean_email(self):
    #     _email = self.cleaned_data.get('email')
    #
    #
    #     return _email
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')



    def login(self):

        pass

__author__ = 'edison'
