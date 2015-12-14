from django.views.generic import CreateView, UpdateView, ListView
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
from apps.seller.models import Seller_Profile
from apps.core.models import GKUser





class SellerForm(ModelForm):
    seller_user_id = IntegerField(required=False)
    class Meta:
        model = Seller_Profile
        fields = ['seller_user_id','seller_name','logo','shop_title', 'shop_link', 'shop_desc', 'status', 'business_section']
        widgets = {
            'seller_user_id': TextInput(attrs={'class': 'user-id-input'}),
            'logo': TextInput(attrs={'class': 'seller-logo-input'})
        }

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
    form_class = SellerCreateForm
    template_name = 'management/create.html'
    model = Seller_Profile




class SellerListView(ListView):
    pass

class SellerUpdateView(UpdateView):
    pass