from django.views.generic import CreateView, UpdateView, ListView
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField,ImageField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.urlresolvers import reverse


from apps.core.utils.image import HandleImage
from apps.seller.models import Seller_Profile
from apps.core.models import GKUser




# TODO : seller is a GKUser,
#        make the connection in UI

class SellerForm(ModelForm):
    seller_user_id = IntegerField(required=False)
    seller_logo_image = ImageField(label='Select an Image', help_text='for Seller logo')

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        # self.fields['seller_user_id'].widget.attrs.update({'class':'user-id-input form-control'})
        self.fields['seller_name'].widget.attrs.update({'class':'form-control'})

        self.fields['logo'].widget.attrs.update({'class':'form-control'})
        self.fields['seller_logo_image'].widget.attrs.update({'class':'form-control'})

        self.fields['shop_title'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_link'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_desc'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control'})
        self.fields['business_section'].widget.attrs.update({'class':'form-control'})
        self.fields['gk_stars'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seller_Profile
        fields = [
                # 'seller_user_id',\
                  'seller_name','logo','seller_logo_image',\
                  'shop_title','shop_link', 'shop_desc', 'status', 'business_section',\
                  'gk_stars'
                  ]

    # def clean_sell_user_id(self):
    #     _user_id = self.cleaned_data.get('seller_user_id')
    #     if not _user_id:
    #         return
    #     try:
    #         _user = GKUser.objects.get(pk=_user_id)
    #     except GKUser.DoesNotExist:
    #         raise ValidationError("can not find user")

    def handle_logo_image(self):
        raise  ImproperlyConfigured


    def save(self, commit=True,*args,**kwargs):
        self.handle_logo_image()
        seller_profile = super(SellerForm,self).save(commit=True,*args,**kwargs)




class SellerCreateForm(SellerForm):

    def clean_seller_logo_image(self):
        _seller_logo_image = self.cleaned_data.get('seller_logo_image')
        if not _seller_logo_image:
            raise ValidationError('need a logo to create seller')
        else:
            return _seller_logo_image

    def handle_logo_image(self):
        _image = HandleImage(image_file=self.cleaned_data.get('seller_logo_image'))
        _image_path = _image.save()
        self.instance.logo = _image_path
        return

class SellerCreateView(CreateView):
    def get_success_url(self):
        return reverse('management_seller_list')
    form_class = SellerCreateForm
    template_name = 'management/seller/create.html'
    model = Seller_Profile




class SellerListView(ListView):
    model = Seller_Profile
    template_name = 'management/seller/list.html'
    context_object_name = 'sellers'
    def get_queryset(self):
        return Seller_Profile.objects.all()


class SellerUpdateView(UpdateView):
    pass

