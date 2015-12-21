from django.views.generic import CreateView, UpdateView, ListView
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from apps.seller.models import Seller_Profile, Seller_Section
from apps.core.models import GKUser





class SellerForm(ModelForm):
    seller_user_id = IntegerField(required=False)\

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        self.fields['seller_user_id'].widget.attrs.update({'class':'user-id-input form-control'})
        self.fields['seller_name'].widget.attrs.update({'class':'form-control'})
        self.fields['logo'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_title'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_link'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_desc'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control'})
        self.fields['business_section'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seller_Profile
        fields = ['seller_user_id','seller_name','logo','shop_title',\
                  'shop_link', 'shop_desc', 'status', 'business_section']

        # widgets = {
        #     'seller_user_id': TextInput(attrs={'class': 'user-id-input form-control'}),
        #     'logo': TextInput(attrs={'class': 'seller-logo-input'})
        # }

    def clean_sell_user_id(self):
        _user_id = self.cleaned_data.get('seller_user_id')
        if not _user_id:
            return

        try:
            _user = GKUser.objects.get(pk=_user_id)
        except GKUser.DoesNotExist:
            raise ValidationError("can not find user")

    def save(self, commit=True,*args,**kwargs):
        seller_profile = super(SellerForm,self).save(commit=True,*args,**kwargs)




class SellerCreateForm(SellerForm):
    pass


class SellerCreateView(CreateView):
    success_url = '/'

    form_class = SellerCreateForm
    template_name = 'management/seller/create.html'
    model = Seller_Profile




class SellerListView(ListView):
    model = Seller_Profile
    template_name = '/management/seller/section_list.html'
    def get_queryset(self):
        return Seller_Profile.objects.filter(status=Seller_Profile.active)


class SellerUpdateView(UpdateView):
    pass


# ====================
# ==== seller section management =====



class SellerSectionCreateView(CreateView):
    template_name = 'management/seller/create_section.html'


class SellerSectionListView(ListView):
    model = Seller_Section
    def get_queryset(self):
        return Seller_Section.objects.filter(active=True)



class SellerSectionUpdateView(UpdateView):
    pass

