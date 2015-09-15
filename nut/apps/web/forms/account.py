from django import forms
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.core.models import GKUser, User_Profile
from apps.core.utils.image import HandleImage

from apps.web.fields import Wizard_CaptchaField
from apps.web.utils.formtools import clean_user_text

from django.utils.log import getLogger
from django.conf import settings

log = getLogger('django')
avatar_path = getattr(settings, 'Avatar_Image_Path', 'avatar/')


class UserSignInForm(forms.Form):

    error_messages = {
        'invalid_login': _('email or password wrong'),
        'inactive': _("This account is inactive."),
        'password_error': _('password error'),
        'no_cookies': _('no cookies'),
    }

    next = forms.CharField(required=False, widget=forms.HiddenInput())

    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': _('Email')}),
        help_text=_('')
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': _('Password')}),
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
        self.next_url = self.cleaned_data.get('next')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login']
                )
            elif self.user_cache.is_active == GKUser.remove:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                self.error_messages['no_cookies']
            )

    def login(self):
        auth_login(self.request, self.user_cache)
        # pass

    def get_next_url(self):

        if self.next_url:
            return self.next_url
        return reverse('web_selection')

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserSignUpForm(forms.Form):

    error_messages = {
        'duplicate_nickname': _("A user with that nickname already exists."),
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    nickname = forms.RegexField(
        error_message=_('nickname: 6 to 30 character can not start with digits'),
        label=_('nickname'),
        regex= r"^[^0-9][\w-]{5,30}$",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('nickname')}),
        help_text=_("Required. 30 characters or fewer. Letters."),
    )

    email = forms.EmailField(
        label=_('email'),
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'hi@guoku.com'}),
        help_text=_('Required.'),
    )

    password = forms.CharField(
        label=_('password'),
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':_('password')}),
        help_text=_('Required')
    )
    confirm_password = forms.CharField(
        label=_('New password confirmation'),
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':_('New password confirmation')}),
        help_text=_("Enter the same password as above, for verification."),
    )

    # we have captcha field now !
    captcha = Wizard_CaptchaField()

    agree_tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked'}), initial=True)

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)


    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        _nickname = clean_user_text(_nickname)
        # print _nickname
        try:
            #  the following line will rise MultipleObjectsReturned if get return more than 1 User_Profile
            #  if this exception is not handled , the exception will simple raise above to cause "internal service error"
            #  right to the user.
            #  so handle it
            User_Profile.objects.get(nickname = _nickname)
        except User_Profile.DoesNotExist:
            return _nickname
        except User_Profile.MultipleObjectsReturned:
            pass
        raise forms.ValidationError(
            self.error_messages['duplicate_nickname'],
            code='duplicate_nickname',
        )

    def clean_email(self):
        _email = self.cleaned_data.get('email')
        # UserModel = get_user_model()
        try:
            GKUser.objects.get(email=_email)
        except GKUser.DoesNotExist:
            return _email
        except GKUser.MultipleObjectsReturned:
            pass
        raise forms.ValidationError(
               self.error_messages['duplicate_email'],
               code='duplicate_email',
            )

    def clean_confirm_password(self):
        self.password = self.cleaned_data.get('password')
        _confirm_password = self.cleaned_data.get('confirm_password')
        if self.password and _confirm_password and self.password != _confirm_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return _confirm_password

    def save(self):
        _nickname = self.cleaned_data.get('nickname')
        _email = self.cleaned_data.get('email')
        _confirm_password = self.cleaned_data.get('confirm_password')

        _user = GKUser.objects.create_user(
            email=_email,
            password = _confirm_password,
            is_active=GKUser.active,
        )

        User_Profile.objects.create(
            user = _user,
            nickname = _nickname,

        )
        _user.send_verification_mail()
        return _user

    def login(self, request, user):
        _user = authenticate(username=user.email, password=self.password)
        auth_login(request, _user)


class UserSignUpBioForm(forms.Form):

    avatar = forms.FileField(
        label=_('avatar'),
        required=False,
    )

    bio = forms.CharField(
        label=_('bio'),
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':'4', 'style':'resize: none;'}),
        help_text=_(''),
        required=False,
    )
    gender = forms.ChoiceField(
        widget = forms.Select(attrs={'class':'form-control'}),
        choices=User_Profile.GENDER_CHOICES,
        label=_('gender'),
        help_text=_(''),
        required=False,
        initial=User_Profile.Man,
    )
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

    def save(self, user):
        _avatar_file = self.cleaned_data.get('avatar')
        _bio = self.cleaned_data.get('bio')
        _bio = clean_user_text(_bio)
        _gender = self.cleaned_data.get('gender')
        _location = self.cleaned_data.get('location')
        _city = self.cleaned_data.get('city')

        # log.info(_avatar)
        self.user = user
        if _avatar_file:
            _image = HandleImage(image_file= _avatar_file)
            _image.crop_square()
            file_path = avatar_path + "%s.jpg" % (_image.name)
            # default_storage.save(file_path, ContentFile(_image.resize(180, 180)))
            avatar = _image.avatar_save(resize=True)
            # avatar = avatar_path + "%s.jpg" % _image.name
            self.user.profile.avatar = avatar
        # else:
        #     avatar = None

        self.user.profile.bio = _bio
        self.user.profile.gender = _gender
        self.user.profile.location = _location
        self.user.profile.city = _city
        self.user.profile.save()


# forget password
# class UserPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(label=_("Email"),
#                              max_length=254,
#                              widget=forms.TextInput(attrs={'class':'form-control'}),
#                              help_text=_('please register email'))
#
#     def __init__(self, *args, **kwargs):
#         super(UserPasswordResetForm, self).__init__(*args, **kwargs)
#         # UserModel = get_user_model()
#
#     def clean_email(self):
#         _email = self.cleaned_data.get('email')
#         UserModel = get_user_model()
#         try:
#             UserModel._default_manager.get(email=_email)
#         except:
#             raise forms.ValidationError(
#                 _('email is not exist')
#             )
#         return _email
#
#
# class UserSetPasswordForm(SetPasswordForm):
#     new_password1 = forms.CharField(label=_("New password"),
#                                     widget=forms.PasswordInput(attrs={'class':'form-control'}),
#                                     help_text=_('New password'))
#     new_password2 = forms.CharField(label=_("New password confirmation"),
#                                     widget=forms.PasswordInput(attrs={'class':'form-control'}),
#                                     help_text=_('New password confirmation'))
#
#     def __init__(self, user, *args, **kwargs):
#
#         super(UserSetPasswordForm, self).__init__(user, *args, **kwargs)


__author__ = 'edison'
