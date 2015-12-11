# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# from apps.core.forms.user import UserForm

from apps.core.models import User_Profile, Buy_Link, Category
from django.utils.log import getLogger

from apps.web.utils.formtools import innerStrip, clean_user_text

log = getLogger('django')


class UserSettingsForm(forms.Form):

    error_messages = {
        'duplicate_email' : _('A user with that email already exists.'),
        'duplicate_nickname': _("A user with that nickname already exists."),

    }

    email = forms.EmailField(label=_('email'),
                             widget=forms.TextInput(attrs={'class':'td', 'type':'email'}),

                             required=False)

    nickname = forms.CharField(label=_('nickname'),
                               widget=forms.TextInput(attrs={'class':'td'}),
                               )

    location = forms.CharField(
        widget=forms.Select(attrs={"name" : "location", "class" : "location"}),
        label=_('location'),
        required=False
    )

    city = forms.CharField(
        widget=forms.Select(attrs={'name' : 'city', 'class' : 'city'}),
        label=_('city'),
        required=False
    )

    gender = forms.ChoiceField(label=_('gender'),
                                choices=User_Profile.GENDER_CHOICES,
                                # widget=forms.Select(attrs={'class':'form-control'}),
                                widget=forms.Select(attrs={'class':'sex td'}))

    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'class':'td'}),
                          required=False,
                          max_length=200
                          )

    website = forms.URLField(label=_('website'),
                             widget=forms.URLInput(attrs={'class':'form-control'}),
                             required=False)
    def clean_nickname(self):
        _nickname = self.cleaned_data.get('nickname')
        _nickname = clean_user_text(_nickname)
        if self.user_cache.profile.nickname == _nickname:
            return _nickname
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
        # return _email

    def clean_bio(self):
        _bio = self.cleaned_data.get('bio')
        # _bio = _bio.replace('\r', '')
        # log.info(_bio)
        s = innerStrip(_bio)
        s = clean_user_text(s)
        # log.info(s)
        return s

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserSettingsForm, self).__init__(*args, **kwargs)

    def save(self):
        _nickname = self.cleaned_data.get('nickname', None)
        _location = self.cleaned_data.get('location', None)
        _city = self.cleaned_data.get('city', None)
        _gender = self.cleaned_data.get('gender', None)
        _bio = self.cleaned_data.get('bio', None)
        _website = self.cleaned_data.get('website', None)
        _email = self.cleaned_data.get('email', None)

        if self.user_cache.email != _email:
            self.user_cache.email = _email
            self.user_cache.profile.email_verified = False

        self.user_cache.profile.nickname = _nickname
        self.user_cache.profile.location = _location
        self.user_cache.profile.city = _city
        self.user_cache.profile.gender = _gender
        self.user_cache.profile.bio = _bio
        self.user_cache.profile.website = _website

        self.user_cache.profile.save()
        self.user_cache.save()


class UserChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_error': _("Old password didn't match")
    }
    current_password = forms.CharField(
        label=_('current password'),
        widget=forms.PasswordInput(attrs={'class':'td','placeholder':_('current password')})
    )

    new_password = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'class':'td','placeholder':_('New password')}),
        min_length=8,
    )

    password_confirmation = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput(attrs={'class':'td','placeholder':_('New password confirmation')}),
        min_length=8,
    )


    def clean_current_password(self):
        _current_password = self.cleaned_data.get('current_password')
        if self.user_cache.check_password(_current_password):
            return _current_password
        else:
            raise forms.ValidationError(
                self.error_messages['password_error'],
                code='password_error'
            )

    def clean_password_confirmation(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('password_confirmation')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def save(self):
        # log.info(self.cleaned_data)
        _password = self.cleaned_data.get('password_confirmation')
        self.user_cache.set_password(_password)
        self.user_cache.save()


ArticleStatusChoice = (
                      # ('all',_('All')),
                       ('selected',_('Selected Article')),
                       ('published',_('Published')),
                        # ('draft', _('Draft')),
                        )
class UserArticleStatusFilterForm(forms.Form):
    articleType = forms.ChoiceField(widget=forms.RadioSelect, choices=ArticleStatusChoice, required=False)
    def get_cleaned_article_status(self):
        if not self.is_valid():
            articleType = 'selected'
        else:
            articleType = self.cleaned_data.get('articleType','selected')
        return articleType



UserLikeEntityCategoryChoice=(
    ('1', '生活日用'),
    ('2','收纳洗晒'),
    ('3','家庭清洁'),
    ('4','室内装饰'),
    ('5','家具'),
    ('6','家电'),
    ('7','烹饪厨具'),
    ('8','个人养护'),
    ('9','外出旅行'),
    ('10','文具'),
    ('11','图书'),
    ('12','食品'),
    ('0','全部'),
)

UserLikeEntityBuyLinkStatusChoice=(
    ('2','正常'),
    ('1','下架'), # Buy_link model has a third state , see implemention in  User Article View
    ('3','全部'),
)

class UserLikeEntityFilterForm(forms.Form):
    entityCategory = forms.ChoiceField(widget=forms.RadioSelect, choices=UserLikeEntityCategoryChoice, required=False)
    entityBuyLinkStatus = forms.ChoiceField(widget=forms.RadioSelect, choices=UserLikeEntityBuyLinkStatusChoice, required=False)
    def get_filter_values(self):
        res = dict()
        if self.is_valid():
            res['entityCategory'] = self.cleaned_data.get('entityCategory', '0')
            res['entityBuyLinkStatus'] = self.cleaned_data.get('entityBuyLinkStatus', '1')
        else:
            res['entityBuyLinkStatus'] = '1'
            res['entityCategory'] =  '0'

        return res




__author__ = 'edison'
