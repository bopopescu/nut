# encoding: utf-8
from apps.core.extend.paginator import ExtentPaginator
from apps.core.views import LoginRequiredMixin
from apps.management.views.entities import Add_local
from braces.views import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from apps.management.forms.sku import SKUForm
from apps.core.models import SKU,Entity
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

class SKUUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        entity = Entity.objects.get(id = self.entity_id)
        sku = SKU.objects.get(pk=self.sku_id)
        return entity in user.entities.all() and sku in entity.skus.all()

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


class SellerEntitySKUCreateView(UserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/create_sku.html'

    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id = self.entity_id)
        return entity in user.entities.all()

    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.entity_id])    #Todo need change

    def get_initial(self):

        return {
            'entity':self.entity_id
        }


class SKUListView(UserPassesTestMixin,ListView):
    template_name = 'web/seller_management/sku_list.html'
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id = self.entity_id)
        return entity in user.entities.all()

    def get_queryset(self):
        entity = self.get_entity()
        return entity.skus.all()

    def get_entity(self):
        return get_object_or_404(Entity, id=self.kwargs.get('entity_id', None))

    def get_context_data(self, **kwargs):
        context = super(SKUListView, self).get_context_data(**kwargs)
        context['entity']= self.get_entity()
        return context

class SKUCreateView(UserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/add_sku.html'
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.get_entity().id])
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id = self.entity_id)
        return entity in user.entities.all()

    def get_initial(self):
        entity = self.get_entity()
        return {
            'entity':entity.id
        }

    def get_entity(self):
        entity_id =  self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

class SKUUpdateView(SKUUserPassesTestMixin,UpdateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/update_sku.html'
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        entity = Entity.objects.get(id = self.entity_id)
        sku = SKU.objects.get(pk=self.sku_id)
        return entity in user.entities.all() and sku in entity.skus.all()

    def get_entity(self):
        entity_id =  self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

    def get_success_url(self):
        return reverse('sku_list_management', args=[self.get_entity().id])


class SKUDeleteView(SKUUserPassesTestMixin, DeleteView):
    model = SKU
    template_name = 'web/seller_management/delete_sku.html'
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        entity = Entity.objects.get(id = self.entity_id)
        sku = SKU.objects.get(pk=self.sku_id)
        return entity in user.entities.all() and sku in entity.skus.all()

    def get_entity(self):
        entity_id =  self.kwargs.get('entity_id')
        entity = get_object_or_404(Entity, id=entity_id)
        return entity

    def get_success_url(self):
        return reverse('sku_list_management', args=[self.get_entity().id])

class SellerEntitySKUCreateView(UserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/create_sku.html'

    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id = self.entity_id)
        return entity in user.entities.all()

    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.entity_id])    #Todo need change

    def get_initial(self):

        return {
            'entity':self.entity_id
        }


