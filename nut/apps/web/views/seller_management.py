from apps.core.extend.paginator import ExtentPaginator
from apps.core.views import LoginRequiredMixin
from apps.management.views.entities import Add_local
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView


class SellerManagement(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 30
    template_name = 'web/seller_management/seller_management.html'

    def get_queryset(self):
        return self.request.user.entities.all()


    def get_context_data(self, **kwargs):
        context = super(SellerManagement, self).get_context_data(**kwargs)
        for entity in context['object_list']:
            entity.sku_list = entity.skus.all()

        return context

    def get(self, request, *args, **kwargs):

        return super(SellerManagement, self).get(request, *args, **kwargs)

class SellerManagementAddEntity(Add_local):
    template_name = 'web/seller_management/add_entity.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web_seller_management'))
        return render(request, self.template_name, {'forms': form})
