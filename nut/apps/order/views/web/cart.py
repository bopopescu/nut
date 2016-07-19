from django.views.generic import ListView
from django.http import  Http404
class UserCartView(ListView):
    template_name = 'web/'

    def get_queryset(self):
        if not self.request.user.is_authenticated():
            raise  Http404
        return self.request.user.cart_items.all()

