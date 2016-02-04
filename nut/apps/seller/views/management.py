import re

from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField,ImageField, URLField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage


from apps.core.models import Article
from apps.core.utils.image import HandleImage
from apps.seller.models import Seller_Profile
from apps.core.models import GKUser


# TODO : seller is a GKUser,
#        make the connection in UI

class SellerForm(ModelForm):
    # seller_user_id = IntegerField(required=False)
    seller_logo_image = ImageField(label='seller_logo_image', help_text='for Seller logo', required=False)
    seller_category_logo_image = ImageField(label='seller Category logo ', help_text='for Seller category logo', required=False)
    related_article_url = URLField(label='interview article address', help_text='FOR SELLER  interview article', required=False)

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        # self.fields['seller_user_id'].widget.attrs.update({'class':'user-id-input form-control'})
        self.fields['seller_name'].widget.attrs.update({'class':'form-control'})

        # self.fields['logo'].widget.attrs.update({'class':'form-control'})
        self.fields['seller_logo_image'].widget.attrs.update({'class':'form-control'})
        self.fields['seller_category_logo_image'].widget.attrs.update({'class':'form-control'})

        self.fields['shop_title'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_link'].widget.attrs.update({'class':'form-control'})
        self.fields['shop_desc'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control'})
        self.fields['business_section'].widget.attrs.update({'class':'form-control'})
        self.fields['gk_stars'].widget.attrs.update({'class':'form-control'})
        self.fields['related_article_url'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seller_Profile
        fields = [
                # 'seller_user_id',\
                  'seller_name','seller_logo_image','seller_category_logo_image',\
                  'shop_title','shop_link', 'shop_desc', 'status', 'business_section',\
                  'gk_stars', 'related_article_url'
                  ]



    def clean_related_article_url(self):
        url = self.cleaned_data.get('related_article_url')
        if not url:
            return None
        p = re.compile(r'articles/(\d+)')
        k = p.search(url)
        if k is None:
            raise ValidationError('can not find article id in URL')
            return None

        article_id = k.group(1)
        try :
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise ValidationError('can not find article object')
            return None

        return url


    def handle_related_article_url(self):

        url = self.cleaned_data.get('related_article_url')
        if not url :
            return

        p = re.compile(r'articles/(\d+)')
        k = p.search(url)
        article_id = k.group(1)
        article = Article.objects.get(pk=article_id)
        self.instance.related_article = article

    def handle_post_image_by_name(self,image_name):
        _image = HandleImage(image_file=self.cleaned_data.get(image_name))
        _image_path = _image.icon_save()
        return _image_path


    def handle_category_logo_image(self):
        image_name = 'seller_category_logo_image'
        if not self.cleaned_data.get(image_name):
            return

        _image_path = self.handle_post_image_by_name(image_name)

        self.instance.category_logo = _image_path

        return



    def handle_logo_image(self):
        image_name =  'seller_logo_image'

        if not self.cleaned_data.get(image_name):
            return

        _image_path = self.handle_post_image_by_name(image_name)
        self.instance.logo = _image_path

        return


    def save(self, commit=True,*args,**kwargs):
        self.handle_logo_image()
        self.handle_category_logo_image()
        self.handle_related_article_url()
        seller_profile = super(SellerForm,self).save(commit=True,*args,**kwargs)




class SellerCreateForm(SellerForm):
    seller_logo_image = ImageField(label='seller_logo_image', help_text='for Seller logo', required=True)
    seller_category_logo_image = ImageField(label='seller Category logo ', help_text='for Seller category logo', required=True)


class SellerUpdateForm(SellerForm):
    seller_logo_image = ImageField(label='seller_logo_image', help_text='for Seller logo', required=False)
    seller_category_logo_image = ImageField(label='seller Category logo ', help_text='for Seller category logo', required=False)


class SellerCreateView(CreateView):
    def get_success_url(self):
        return reverse('management_seller_list')
    form_class = SellerCreateForm
    template_name = 'management/seller/create.html'
    model = Seller_Profile

class SellerListView(ListView):
    paginate_by = 25
    paginator_class = ExtentPaginator
    model = Seller_Profile
    template_name = 'management/seller/list.html'
    context_object_name = 'sellers'
    def get_queryset(self):
        return Seller_Profile.objects.all()


class SellerUpdateView(UpdateView):
    def get_success_url(self):
        return reverse('management_seller_list')
    form_class = SellerUpdateForm
    model = Seller_Profile
    template_name = 'management/seller/edit.html'


# class SellerDeleteView(DeleteView):
#     model = Seller_Profile
#     def get_success_url(self):
#         return reverse('management_seller_list')
