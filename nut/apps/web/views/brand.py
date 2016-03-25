from django.core.paginator import EmptyPage
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.core.models import Brand, Entity_Like
from braces.views import AjaxResponseMixin
from braces.views import JSONResponseMixin
from django.template import loader
from django.template import RequestContext
from apps.core.utils.http import JSONResponse

# TODO Brand front end view
from core.extend.paginator import ExtentPaginator, PageNotAnInteger


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

    def get_queryset(self):
        brand_pk = self.kwargs.get('pk')
        brand = get_object_or_404(Brand, pk=brand_pk)
        sqs = brand.entities
        return sqs

    def get_context_data(self,*args, **kwargs):
        brand_pk = self.kwargs.get('pk')
        context = super(BrandDetailView, self).get_context_data(*args,**kwargs)
        context['brand'] = get_object_or_404(Brand, pk=brand_pk)

        el = list()
        sqs = self.get_queryset()
        e_ids = [e.entity_id for e in sqs]
        if self.request.user.is_authenticated():
             el = Entity_Like.objects.user_like_list(user=self.request.user,
                                                    entity_list=e_ids
                                                    ).using('slave')
        context['user_entity_likes'] = el
        return context
