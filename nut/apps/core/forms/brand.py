from django import forms
from django.utils.translation import gettext_lazy as _
from apps.core.models import Brand
from urlparse import urlparse, parse_qs
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
#
# from apps.core.utils.image import HandleImage
#
# from django.conf import settings
#
# image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class BrandForm(forms.Form):
    error_messages = {
        'duplicate_brand_name': _("Brand name already exists."),
        # 'password_mismatch': _("The two password fields didn't match."),
    }


    icon = forms.FileField(
        label=_('icon'),
        widget=forms.FileInput(),
        help_text=_('icon need 300 x 300'),
        required=False,
    )

    name = forms.CharField(
        label=_('brand name'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('brand name'),
    )

    alias = forms.CharField(
        label=_('alias'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('optional'),
        required=False,
    )

    national = forms.CharField(
        label=_('national'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        # required=False,
    )

    company = forms.CharField(
        label=_('company'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('optional'),
        required=False,
    )

    website = forms.URLField(
        label=_('website'),
        widget=forms.URLInput(attrs={'class':'form-control'}),
        help_text=_('prefix has http://'),
        required=False,
    )

    tmall_link = forms.URLField(
        label=_('tmall link'),
        widget=forms.URLInput(attrs={'class':'form-control'}),
        help_text=_('brand tmall shop link'),
        required=False,
    )

    status = forms.ChoiceField(label=_('status'),
                                choices=Brand.BRAND_STATUS_CHOICES,
                                widget=forms.Select(attrs={'class':'form-control'}),
                                initial=Brand.pending,
                                help_text=_('status'))

    score = forms.IntegerField(label=_('brand score'),
                                 initial= 0 ,
                                 help_text=_('input a score of the brand')
                                )

    intro = forms.CharField(
        label=_('intro'),
        widget=forms.Textarea(attrs={'class':'form-control'}),
        # min_length=300,
        max_length=1000,
        help_text=_('300 - 1000 words'),
        required=False,
    )

    def clean_name(self):
        _name = self.cleaned_data.get('name')
        _name = _name.strip(' \t\n\r')

        try:
            Brand.objects.get(name=_name)
        except Brand.DoesNotExist:
            return _name

        raise forms.ValidationError(
            self.error_messages['duplicate_brand_name'],
            code='duplicate_brand_name',
        )

    def cleaned_alias(self):
        _alias = self.cleaned_data.get('alias')
        return _alias.strip(' \t\n\r')

    def cleaned_national(self):
        _national = self.cleaned_data.get('national')
        return _national.strip(' \t\n\r')

    def cleaned_company(self):
        _company = self.cleaned_data.get('company')
        return _company.strip(' \t\n\r')

    def clean_intro(self):
        _intro = self.cleaned_data.get('intro')
        return _intro.strip(' \t\n\r')

    def clean_tmall_link(self):
        _tmall_link = self.cleaned_data.get('tmall_link', None)
        # print _tmall_link
        # if len(_tmall_link) == 0:
        #     return _tmall_link
        #
        # urlobj = urlparse(_tmall_link)
        # qs = parse_qs(urlobj.query)
        # link = "%s://%s%s?shop_id=%s" % (urlobj.scheme, urlobj.hostname, urlobj.path, qs['shop_id'][0])
        return _tmall_link.strip(' \t\n\r')

    #
    # def __init__(self, brand, *args, **kwargs):
    #     self.brand_cache = brand
    #     super(BrandForm, self).__init__(*args, **kwargs)

    def save(self):

        pass


__author__ = 'edison'
