from apps.core.extend.paginator import ExtentPaginator
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.order.models import OrderItem
from apps.core.models import Entity
from apps.order.models import SKU,Order

from django.views.generic import ListView, DetailView


class OrderListView(FilterMixin, SortMixin, ListView):
    default_sort_params = ('dnumber','desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'management/management_order_list.html'

    def get_queryset(self):
        entities = self.request.user.entities.all()
        order_items = OrderItem.objects.filter(sku__entity_id__in=entities)
        order_ids = order_items.values_list('order')
        qs = Order.objects.all()
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1,2,4])
        elif self.status == 'paid':
            qs = qs.filter(status=3)
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        #if filter_field == 'id':
            #qs = qs.filter(id=filter_value.strip())
        if filter_field == 'number':
            qs = qs.filter(number__icontains=filter_value.strip())
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'dprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=True)
        elif sort_by == 'uprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=False)
        elif sort_by == 'dnumber':
            qs = qs.order_by('-number')
        elif sort_by == 'unumber':
            qs = qs.order_by('number')
        elif sort_by == 'status':
            qs =  qs.order_by('-status')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['status'] = self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count = order.items.all().count()
            order.itemslist = order.items.all()[1:order.count]
        return context


class SoldEntityListView(FilterMixin, SortMixin, ListView):
    default_sort_params = ('dstock', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 10
    template_name = 'management/management_sold_entity_list.html'

    def get_queryset(self):
        self.orders = Order.objects.filter(status__in=[3, 5])
        sku_ids = []
        if self.orders:
            for order in self.orders:
                if sku_ids:
                    sku_ids += list(order.items.values_list('sku'))
                else:
                    sku_ids = list(order.items.values_list('sku'))
        if sku_ids:
            for i in range(len(sku_ids)):
                sku_ids[i]=sku_ids[i][0]
        #sku_ids = self.order_items.values_list('sku')
        qs = SKU.objects.filter(id__in=sku_ids)
        # qs = list(set([item.sku for item in self.order_items]))
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def sort_queryset(self, qs, sort_by, order):
        d={}
        for ord in self.orders:
            for order in ord.items.all():
                if order.sku.id not in d.keys():
                    d[order.sku.id] = order.volume
                else:
                    d[order.sku.id] += order.volume
        if qs:
            for i in qs:
                if i.id in d.keys():
                    i.sold_count=d[i.id]
                else:
                    i.sold_count=0
        if sort_by == 'dsold_count':
            qs = sorted(qs, key=lambda x: x.sold_count, reverse=True)
        elif sort_by == 'usold_count':
            qs = sorted(qs, key=lambda x: x.sold_count, reverse=False)
        elif sort_by == 'dstock':
            qs = qs.order_by('-stock')
        elif sort_by == 'ustock':
            qs = qs.order_by('stock')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(SoldEntityListView, self).get_context_data(**kwargs)
        for sku in context['object_list']:
            sku.title=sku.entity.title[:15]

        d = {}
        for ord in self.orders:
            for order in ord.items.all():
                if order.sku.id not in d.keys():
                    d[order.sku.id] = order.volume
                else:
                    d[order.sku.id] += order.volume
        for object in context['object_list']:
            object.sold_count = d[object.id]
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(entity__title__icontains=filter_value.strip())
        else:
            pass
        return qs


class ManagementOrderDetailView(DetailView):
    pk_url_kwarg = 'order_number'
    context_object_name = 'order'
    model = Order
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 10
    template_name = 'management/management_order_detail.html'

    def get_context_data(self, **kwargs):
        self.order_number = self.kwargs.get('order_number')
        context = super(ManagementOrderDetailView, self).get_context_data(**kwargs)
        context['order_item'] = context['order'].items.all()
        # context['order_item'] = context['order'].items.all()
        context['order_number'] = self.order_number
        context['promo_total_price'] = context['order'].promo_total_price
        context['origin_total_price'] = context['order'].grand_total_price
        context['count'] = context['order'].items.all().count()
        return context
