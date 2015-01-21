from django import forms
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
    email = forms.EmailField(
        widget=forms.EmailInput(),
        required=False,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        min_length=8,
    )

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(MobileUserProfileForm, self).__init__(*args, **kwargs)

    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
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

    def save(self):
        _image = self.cleaned_data.get('image')
        _nickname = self.cleaned_data.get('nickname')
        _email = self.cleaned_data.get('email')
        # print _nickname
        if _image:
            avatar_file = HandleImage(_image)

            self.user_cache.profile.avatar = avatar_file.avatar_save()
        if _nickname:
            self.user_cache.profile.nickname = _nickname

        self.user_cache.profile.save()
        return self.user_cache.v3_toDict()

__author__ = 'edison7500'
