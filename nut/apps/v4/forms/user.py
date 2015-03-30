from django import forms
from django.contrib.auth import get_user_model
from apps.core.models import User_Profile
from apps.core.utils.image import HandleImage


class MobileUserProfileForm(forms.Form):

    image = forms.FileField(
        required=False
    )
    nickname = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )
    # email = forms.EmailField(
    #     widget=forms.EmailInput(),
    #     required=False,
    # )

    bio = forms.CharField(
        widget=forms.Textarea(),
        max_length=30,
        required=False,
    )
    gender = forms.ChoiceField(
        choices=User_Profile.GENDER_CHOICES,
        widget=forms.RadioSelect(),
        required=False,
    )
    location = forms.CharField(
        widget=forms.TextInput(),
        required=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(MobileUserProfileForm, self).__init__(*args, **kwargs)

    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        if _nickname == self.user_cache.profile.nickname:
            return _nickname

        if _nickname:
            try:
                User_Profile.objects.get(nickname = _nickname)
            except User_Profile.DoesNotExist:
                return _nickname
            raise forms.ValidationError(
                self.error_messages['duplicate_nickname'],
                code='duplicate_nickname',
            )

    # def clean_email(self):
    #     _email = self.cleaned_data.get('email')
    #
    #     if _email is None:
    #         return None
    #
    #     if self.user_cache.email == _email:
    #         return _email
    #
    #     try:
    #         get_user_model()._default_manager.get(email = _email)
    #     except get_user_model().DoesNotExist:
    #         return _email
    #     raise forms.ValidationError(
    #         self.error_messages['duplicate_email'],
    #         code= 'duplicate_email',
    #     )

    def save(self):
        _image = self.cleaned_data.get('image')
        _nickname = self.cleaned_data.get('nickname')
        _bio = self.cleaned_data.get('bio')
        _gender = self.cleaned_data.get('gender')
        _location = self.cleaned_data.get('location')
        # print _nickname
        if _image:
            avatar_file = HandleImage(_image)

            self.user_cache.profile.avatar = avatar_file.avatar_save()

        if _nickname:
            self.user_cache.profile.nickname = _nickname

        if _gender:
            self.user_cache.profile.gender = _gender

        if _location:
            self.user_cache.profile.location = _location
        # if _email:
        #     self.user_cache.email = _email
        #     self.user_cache.save()
        #
        # if _password:
        #     self.user_cache.set_password(_password)
        #     self.user_cache.save()

        if _bio:
            self.user_cache.profile.bio = _bio

        self.user_cache.profile.save()
        return self.user_cache.v3_toDict()

__author__ = 'edison7500'
