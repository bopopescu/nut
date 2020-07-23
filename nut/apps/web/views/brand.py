from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from apps.core.models import Brand, Entity_Like, Entity_Brand


class BrandListView(ListView):
    model = Brand
    template_name = 'web/brand/list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.all()


class BrandDetailView(ListView):
    template_name = 'web/brand/detail.html'
    paginate_by = 24
    context_object_name = 'entities'

    def get_order_by(self):
        order_by = self.kwargs.get('order_by', 'pub_time')
        return order_by

    def get_queryset(self):
        brand_pk = self.kwargs.get('pk')
        entity_brand = Entity_Brand.objects.filter(brand_id=int(brand_pk)).order_by('brand_order')
        if self.get_order_by() == 'olike':
            sqs = sorted(entity_brand, key=lambda x: x.entity.like_count, reverse=True)
        else:
            sqs = sorted(entity_brand, key=lambda x: (x.brand_order, x.entity.created_time))

        return sqs

    def get_context_data(self, *args, **kwargs):
        brand_pk = self.kwargs.get('pk')
        context = super(BrandDetailView, self).get_context_data(*args, **kwargs)
        context['brand'] = get_object_or_404(Brand, pk=brand_pk)
        context['pk'] = brand_pk
        context['sort_method'] = self.get_order_by()

        el = []
        e_ids = [e.entity.id for e in self.object_list]
        if self.request.user.is_authenticated():
            el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=e_ids
                                                    ).using('subordinate')
        context['user_entity_likes'] = el
        return context
