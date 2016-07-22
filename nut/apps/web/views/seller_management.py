# encoding: utf-8
from apps.core.extend.paginator import ExtentPaginator
from apps.core.forms.entity import EditEntityForm
from apps.core.mixins.views import FilterMixin
from apps.core.views import LoginRequiredMixin
from apps.management.views.entities import Add_local
from braces.views import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from apps.management.forms.sku import SKUForm
from apps.core.models import SKU,Entity
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.http import Http404

class SKUUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        entity = Entity.objects.get(id = self.entity_id)
        sku = SKU.objects.get(pk=self.sku_id)
        return entity in user.entities.all() and sku in entity.skus.all()
    def no_permissions_fail(self, request=None):
        raise Http404

class EntityUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id=self.entity_id)
        return entity in user.entities.all()
    def no_permissions_fail(self, request=None):
        raise Http404

class SellerManagement(LoginRequiredMixin, FilterMixin, ListView):
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 10
    template_name = 'web/seller_management/seller_management.html'

    def get_queryset(self):
        qs = self.request.user.entities.all()
        return self.filter_queryset(qs,self.get_filter_param())

    def get_context_data(self, **kwargs):
        context = super(SellerManagement, self).get_context_data(**kwargs)
        for entity in context['object_list']:
            entity.sku_list = entity.skus.all()
            entity.title=entity.title[:15]
        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(title__icontains=filter_value.strip())
        # elif filter_field == 'title':
        #     qs = qs.filter(title__icontains=filter_value.strip())
        else:
            pass
        return qs



class SellerManagementAddEntity(Add_local):
    template_name = 'web/seller_management/add_entity.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web_seller_management'))
        return render(request, self.template_name, {'forms': form})

@login_required
def seller_management_entity_edit(request, entity_id, template='web/seller_management/edit_entity.html'):
    #Todo 拆分模版, 重写view
    _update = None
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404
    data = {
        # 'id':entity.pk,
        'creator': entity.user.profile.nickname,
        'brand': entity.brand,
        'title': entity.title,
        'price': entity.price,
        'status': entity.status,
        'category': entity.category.group_id,
        'sub_category': entity.category_id,
    }

    if request.method == "POST":
        _forms = EditEntityForm(
            entity,
            request.POST,
            initial=data
        )
        _update = 1

        if _forms.is_valid():
            _forms.save()
            _update = 0

    else:
        _forms = EditEntityForm(
            entity=entity,
            initial=data
        )

    return render_to_response(
        template,
        {
            'entity': entity,
            'forms': _forms,
            'update': _update,
        },
        context_instance=RequestContext(request)
    )


class SellerEntitySKUCreateView(EntityUserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/create_sku.html'
    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.entity_id])    #Todo need change

    def get_initial(self):
        return {
            'entity':self.entity_id
        }

class SKUListView(EntityUserPassesTestMixin,ListView):
    template_name = 'web/seller_management/sku_list.html'
    def get_queryset(self):
        entity = get_object_or_404(Entity, id=self.entity_id)
        return entity.skus.all()
    def get_context_data(self, **kwargs):
        context = super(SKUListView, self).get_context_data(**kwargs)
        context['entity']= get_object_or_404(Entity, id=self.entity_id)
        return context

class SKUCreateView(EntityUserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/add_sku.html'
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])
    def get_context_data(self, **kwargs):
        context = super(CreateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_initial(self):
        return {
            'entity':self.entity_id
        }

class SKUUpdateView(SKUUserPassesTestMixin,UpdateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/update_sku.html'
    def get_context_data(self, **kwargs):
        context = super(SKUUpdateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])


class SKUDeleteView(SKUUserPassesTestMixin, DeleteView):
    model = SKU
    template_name = 'web/seller_management/delete_sku.html'

    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])




