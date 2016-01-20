from django import forms
from django.forms import ModelForm ,BooleanField


from apps.core.models import GKUser, Authorized_User_Profile

class UserAuthorInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAuthorInfoForm, self).__init__(*args, **kwargs)
        self.fields['weixin_id'].widget.attrs.update({'class':'form-control'})
        self.fields['weixin_nick'].widget.attrs.update({'class':'form-control'})
        self.fields['author_website'].widget.attrs.update({'class':'form-control'})
        self.fields['weibo_id'].widget.attrs.update({'class':'form-control'})
        self.fields['weibo_nick'].widget.attrs.update({'class':'form-control'})
        self.fields['personal_domain_name'].widget.attrs.update({'class':'form-control'})
    class Meta:
        model = Authorized_User_Profile
        fields = [
                  'weixin_id', 'weixin_nick','weixin_qrcode_img',\
                  'author_website','weibo_id','weibo_nick','personal_domain_name'
                  ]

    def clean_personal_domain_name(self):

        data = self.cleaned_data['personal_domain_name']
        if len(data) < 5 or len(data) >15 :
            raise forms.ValidationError('personal domain length must between 5-15')
        return data

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
