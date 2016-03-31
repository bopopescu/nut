from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.core.models import Brand, Entity_Like, Entity
from haystack.query import SearchQuerySet


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
        brand = get_object_or_404(Brand, pk=brand_pk)

        if self.get_order_by() == 'olike':
            sqs = SearchQuerySet().models(Entity).filter(brand=brand.name).order_by('like_count')
        else:
            sqs = SearchQuerySet().models(Entity).filter(brand=brand.name).order_by('-created_time')

        return sqs

    def get_context_data(self,*args, **kwargs):
        brand_pk = self.kwargs.get('pk')
        context = super(BrandDetailView, self).get_context_data(*args,**kwargs)
        context['brand'] = get_object_or_404(Brand, pk=brand_pk)
        context['pk'] = brand_pk
        context['sort_method'] = self.get_order_by()

        el = list()
        sqs = self.get_queryset()
        e_ids = [e.entity_id for e in sqs]
        if self.request.user.is_authenticated():
             el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=e_ids
                                                    ).using('slave')
        context['user_entity_likes'] = el
        return context





    # def get_queryset(self):
    #     cid = self.get_category_id()
    #     order_by_like = False
    #     if self.get_order_by() == 'olike':
    #         order_by_like = True
    #     self.cid = cid
    #     entity_list = Entity.objects.sort(category_id=cid,
    #                                       like=order_by_like).exclude(
    #         selection_entity__is_published=False)
    #     return entity_list
    #
    #
    #     order_by_like = False
    #     if self.get_order_by() == 'olike':
    #         order_by_like = True


