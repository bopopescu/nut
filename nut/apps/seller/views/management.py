from django.views.generic import CreateView, UpdateView, ListView
from apps.seller.models import Seller_Profile

class SellerCreateView(CreateView):
    template_name = ''
    model = Seller_Profile
    fields = ['user', 'shop_title','seller_name', \
              'shop_desc', 'status', 'logo', 'business_section']




class SellerListView(ListView):
    pass

class SellerUpdateView(UpdateView):
    pass