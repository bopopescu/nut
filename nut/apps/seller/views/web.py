from django.views.generic import TemplateView
from django.forms import ModelForm, TextInput
from django.forms.fields import IntegerField
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError
from apps.seller.models import Seller_Profile
from apps.core.models import GKUser


class SellerView(TemplateView):

    template_name = 'web/seller/web_seller.html'

    def get_context_data(self, **kwargs):
        super(SellerView, self).get_context_data(**kwargs)



