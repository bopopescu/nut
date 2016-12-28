import re

from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView
from django import forms
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField,ImageField, URLField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage


from apps.core.models import Article
from apps.core.utils.image import HandleImage
from apps.seller.models import Seller_Profile,IndexPageMeta
from apps.core.models import GKUser


# TODO : seller is a GKUser,
#        make the connection in UI
from apps.core.mixins.views import ExtraQueryMixin


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
        # self.fields['is2016store'].widget.attrs.update({'class':'form-control'})
        # self.fields['is2015store'].widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Seller_Profile
        fields = [
                # 'seller_user_id',\
                  'seller_name','seller_logo_image','seller_category_logo_image',\
                  'shop_title','shop_link', 'shop_desc', 'status', 'business_section',\
                  'gk_stars', 'related_article_url', 'is2016store', 'is2015store'
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


class SellerListView(ExtraQueryMixin, ListView):
    paginate_by = 100
    paginator_class = ExtentPaginator
    model = Seller_Profile
    template_name = 'management/seller/list.html'
    context_object_name = 'sellers'


    def get_queryset(self):
        year = self.request.GET.get('year')
        if year == '2015':
            self.extra_query_dic['year'] = 2015
            return Seller_Profile.objects.filter(is2015store=True).order_by('-id')
        elif year == '2016':
            self.extra_query_dic['year'] = 2016
            return Seller_Profile.objects.filter(is2016store=True).order_by('-id')
        else:
            self.extra_query_dic['year'] = 'all'
            return Seller_Profile.objects.all().order_by('-id')


class SellerUpdateView(UpdateView):
    def get_success_url(self):
        return reverse('management_seller_list')
    form_class = SellerUpdateForm
    model = Seller_Profile
    template_name = 'management/seller/edit.html'



class Index2016ContentForm(ModelForm):
    writer_list = forms.CharField(
        label = _("writer_list"),
        widget= forms.Textarea()
    )
    topic_tag_list = forms.CharField(
        label= _("topic_tag_list"),
        widget= forms.Textarea
    )

    column_article_tag_list = forms.CharField(
        label= _("topic_tag_list"),
        widget= forms.Textarea
    )

    def clean_writer_list(self):
        return [1, 2, 3]

    def save(self):
        ins = super(Index2016ContentForm, self).save()
        ins.writer_list = [1, 2, 3]
        ins.save()


    class Meta:
        model = IndexPageMeta
        fields = ['writer_list', 'topic_tag_list', 'column_article_tag_list']


class Store2016IndexManageView(UpdateView):
    template_name = 'management/seller/meta_2016.html'
    form_class = Index2016ContentForm
    model = IndexPageMeta

    def get_success_url(self):
        return reverse('management_2016_store_index')

    def get_object(self, queryset=None):
        obj, created = IndexPageMeta.objects.get_or_create(year='2016')
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(Store2016IndexManageView, self).get_context_data(*args, **kwargs)
        return context

# class SellerDeleteView(DeleteView):
#     model = Seller_Profile
#     def get_success_url(self):
#         return reverse('management_seller_list')
