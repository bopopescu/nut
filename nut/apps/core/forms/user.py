from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.log import getLogger
from django.contrib.auth.forms import SetPasswordForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

log = getLogger('django')


from apps.core.models import User_Profile
from apps.core.utils.image import HandleImage



class UserForm(forms.Form):
    YES_OR_NO = (
        (True, _('yes')),
        (False, _('no')),
    )

    error_messages = {
        'duplicate_email' : _('A user with that email already exists.'),
    }

    # user_id = forms.CharField(label=_('user_id'),
    #                           widget=forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
    #                           )
    email = forms.EmailField(label=_('email'),
                             widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
                             )
    nickname = forms.CharField(label=_('nickname'),
                               widget=forms.TextInput(attrs={'class':'form-control'}),
                               )

    is_active = forms.ChoiceField(label=_('user group'),
                                  choices=get_user_model().USER_STATUS_CHOICES,
                                   widget=forms.Select(attrs={'class':'form-control'}),
                                   required=False,
                                   )
    # is_active = forms.ChoiceField(label=_('active'),
    #                                 choices=YES_OR_NO,
    #                                 widget=forms.Select(attrs={'class':'form-control'}),
    #                                 )
    is_admin = forms.BooleanField(label=_('admin'),
                                   widget=forms.RadioSelect(choices=YES_OR_NO),
                                   required=False,
                                   )
    # is_admin = forms.ChoiceField(label=_('admin'),
    #                              choices=YES_OR_NO,
    #                              widget=forms.Select(attrs={'class':'form-control'}),
    #                              )

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
                                initial=User_Profile.Other,
                                )

    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'class':'form-control','rows':'4', 'style':'resize:none;'}),
                          required=False,
                          max_length=200,
                          )

    website = forms.URLField(label=_('website'),
                             widget=forms.TextInput(attrs={'class':'form-control'}),
                             required=False,
                             )

    def __init__(self, user, *args, **kwargs):
        # self.request = request
        self.user_cache = user
        super(UserForm, self).__init__(*args, **kwargs)

    # def clean_user_id(self):
    #     _user_id = self.cleaned_data.get('user_id')
    #     self.user_cache = get_user_model()._default_manager.get(pk = _user_id)
    #
    #     return _user_id

    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        # print _nickname
        if self.user_cache.profile.nickname == _nickname:
            return _nickname

        try:
            User_Profile.objects.get(nickname = _nickname)
        except User_Profile.DoesNotExist:
            return _nickname
        raise forms.ValidationError(
            self.error_messages['duplicate_nickname'],
            code='duplicate_nickname',
        )

    def clean_email(self):

        _email = self.cleaned_data.get('email')
        if self.user_cache.email == _email:
            return _email

        try:
            get_user_model()._default_manager.get(email = _email)
        except get_user_model().DoesNotExist:
            return _email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code= 'duplicate_email',
        )
        # return self.cleaned_data


    def save(self):

        # user = GKUser.objects.get(pk = _user_id)
        # user = get_user_model()._default_manager.get(pk = _user_id)
        self.user_cache.is_active = self.cleaned_data.get('is_active')
        self.user_cache.is_admin = self.cleaned_data.get('is_admin')
        self.user_cache.email = self.clean_email()
        self.user_cache.profile.nickname = self.cleaned_data['nickname']
        self.user_cache.profile.gender = self.cleaned_data['gender']
        self.user_cache.profile.website = self.cleaned_data['website']
        self.user_cache.profile.bio = self.cleaned_data['bio']
        self.user_cache.profile.save()
        self.user_cache.save()

        return self.user_cache


class GuokuSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New password'),
                                      widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                      )
    new_password2 = forms.CharField(label=_('New password confirmation'),
                                       widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                       )


class AvatarForm(forms.Form):

    avatar_file = forms.ImageField(
                        label='Select an Image',
                        help_text=_('max. 2 megabytes'))


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AvatarForm, self).__init__(*args, **kwargs)

    def save(self):
        # self.user = user
        _avatar_file = self.cleaned_data.get('avatar_file')
        # log.info(_avatar_file)
        _image = HandleImage(image_file= _avatar_file)

        avatar_path_name = _image.avatar_save()

        self.user.profile.avatar = avatar_path_name

        self.user.profile.save()


__author__ = 'edison'
