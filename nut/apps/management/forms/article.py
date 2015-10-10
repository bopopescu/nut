from django.forms import ModelForm
from django import forms
from apps.core.models import Article, GKUser
from apps.core.forms import get_admin_user_choices , get_author_choices
from django.utils.translation import gettext_lazy as _

class UsernameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.profile.nickname

class UpdateArticleForm(ModelForm):

    tags = forms.CharField(
        label=_('tags'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='',
        required=False,
    )
    creator = UsernameChoiceField(queryset=GKUser.objects.author())


    class Meta:
        model = Article
        fields = ['publish', 'read_count', 'creator']


