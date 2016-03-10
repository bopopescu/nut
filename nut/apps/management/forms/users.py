# -*- coding: utf-8 -*-
import re
from django import forms
from django.forms import ModelForm ,BooleanField, CharField, HiddenInput



from apps.core.models import GKUser, Authorized_User_Profile
from apps.shop.models import Shop


class UserAuthorInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAuthorInfoForm, self).__init__(*args, **kwargs)
        self.fields['weixin_id'].widget.attrs.update({'class':'form-control'})
        self.fields['weixin_nick'].widget.attrs.update({'class':'form-control'})
        self.fields['author_website'].widget.attrs.update({'class':'form-control'})
        self.fields['weibo_id'].widget.attrs.update({'class':'form-control'})
        self.fields['weibo_nick'].widget.attrs.update({'class':'form-control'})
        self.fields['personal_domain_name'].widget.attrs.update({'class':'form-control'})
        self.fields['points'].widget.attrs.update({'class':'form-control'})
        self.fields['rss_url'].widget.attrs.update({'class':'form-control'})
    class Meta:
        model = Authorized_User_Profile
        fields = [
                  'weixin_id', 'weixin_nick','weixin_qrcode_img',\
                  'author_website','rss_url',\
                  'weibo_id','weibo_nick','personal_domain_name',\
                  'points','is_recommended_user',
                  ]

    def clean_personal_domain_name(self):

        person_domain = self.cleaned_data['personal_domain_name']

        if len(person_domain) < 5 or len(person_domain) >30 :
            raise forms.ValidationError('personal domain length must between 5-30')

        if re.match(r"^[a-z][a-z0-9]{4,14}$", person_domain) is None:
            raise forms.ValidationError('personal domain must be all english char or digit,and  NOT start with a digit')

        try:
            profile = Authorized_User_Profile.objects.get(personal_domain_name=person_domain, )
        except Authorized_User_Profile.DoesNotExist as e:
        #     ok here no duplicate; clean!!!!
            return person_domain
        except Authorized_User_Profile.MultipleObjectsReturned as e:
        #     not good  , already has the same domain
            raise forms.ValidationError('domain already exist !!! try another one')

        # already have the domain in profile ,
        #  is it the users currnet one?
        if self.instance.personal_domain_name == person_domain:
            # same as before , just ok and return
            return person_domain
        else:
            # domain changed and collide with other's domain
            raise forms.ValidationError('domain already exist!!! try another one')

        return person_domain

class UserAuthorSetForm(ModelForm):
    isAuthor = BooleanField(required=False)
    # http://stackoverflow.com/questions/31349584/appending-formdata-field-with-value-as-a-boolean-false-causes-the-function-to-fa
    def __init__(self,*args, **kwargs):
        super(UserAuthorSetForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        _user = self.instance
        _user.setAuthor(self.cleaned_data.get('isAuthor'))

    class Meta:
        model = GKUser
        fields = ['isAuthor']

class UserSellerSetForm(ModelForm):
    isSeller = BooleanField(required=False)
    class Meta:
        model = GKUser
        fields = ['isSeller']

    def save(self,commit=True):
        _user = self.instance
        _user.setSeller(self.cleaned_data.get('isSeller'))

class SellerShopForm(ModelForm):
    owner =  CharField(required=True, widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SellerShopForm, self).__init__(*args, **kwargs)
        for key , field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

    def clean_owner(self):
        _owner_id = self.cleaned_data.get('owner')
        _owner = GKUser.objects.get(pk=_owner_id)
        return _owner

    class Meta:
        model = Shop
        fields = ['owner','shop_title', 'shop_link', 'shop_style', 'shop_type']