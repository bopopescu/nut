from django import forms
from django.utils.translation import gettext_lazy as _

# from apps.core.forms.user import UserForm
from apps.core.models import User_Profile



class UserSettingsForm(forms.Form):
    email = forms.EmailField(label=_('email'),
                             widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
                             help_text=_(''),
                             required=False)

    nickname = forms.CharField(label=_('nickname'),
                               widget=forms.TextInput(attrs={'class':'form-control'}),
                               help_text=_(''))

    location = forms.CharField(
        widget=forms.Select(attrs={"name" : "location", "class" : "form-control location"}),
        label=_('location'),
        required=False
    )

    city = forms.CharField(
        widget=forms.Select(attrs={'name' : 'city', 'class' : 'form-control city'}),
        label=_('city'),
        required=False
    )

    gender = forms.ChoiceField(label=_('gender'),
                                choices=User_Profile.GENDER_CHOICES,
                                # widget=forms.Select(attrs={'class':'form-control'}),
                                widget=forms.RadioSelect(),
                                help_text=_(''))
    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'class':'form-control','rows':'4', 'style':'resize:none;'}),
                          required=False,
                          help_text=_(''))
    website = forms.URLField(label=_('website'),
                             widget=forms.TextInput(attrs={'class':'form-control'}),
                             required=False,
                             help_text=_(''))


    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserSettingsForm, self).__init__(*args, **kwargs)

    def save(self):
        _nickname = self.cleaned_data.get('nickname', None)
        _location = self.cleaned_data.get('location', None)
        _city = self.cleaned_data.get('city', None)

        self.user_cache.profile.nickname = _nickname
        self.user_cache.profile.location = _location
        self.user_cache.profile.city = _city
        self.user_cache.profile.save()

__author__ = 'edison'
