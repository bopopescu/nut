from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.core.extend.paginator import ExtentPaginator
from apps.shop.models import StorePageBanners, StorePageRecommend
from django.core.urlresolvers import reverse_lazy

from apps.banners.forms import BaseBannerForm,\
                               BaseBannerCreateForm,\
                               BaseBannerUpdateForm

from braces.views import StaffuserRequiredMixin

class StoreBannerCreateForm(BaseBannerCreateForm):
    class Meta:
        model = StorePageBanners
        fields = BaseBannerForm.default_banner_fields

class StoreBannerUpdateForm(BaseBannerUpdateForm):
    class Meta:
        model = StorePageBanners
        fields = BaseBannerForm.default_banner_fields


class StoreRecommendCreateForm(BaseBannerCreateForm):
    class Meta:
        model = StorePageRecommend
        fields = BaseBannerForm.default_banner_fields

class StoreRecommendUpdateForm(BaseBannerUpdateForm):
    class Meta:
        model = StorePageBanners
        fields = BaseBannerForm.default_banner_fields

class StoreBannerListView(StaffuserRequiredMixin,ListView):
    template_name = 'management/shop/Store_banner_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  StorePageBanners
    context_object_name = 'banners'
    def get_queryset(self):
        return StorePageBanners.objects.all()

class StoreBannerCreateView(StaffuserRequiredMixin,CreateView):
    form_class = StoreBannerCreateForm
    model = StorePageBanners
    template_name = 'management/shop/Store_banner_create.html'
    success_url = reverse_lazy('manage_store_banners')

class StoreBannerUpdateView(StaffuserRequiredMixin, UpdateView):
    form_class  = StoreBannerUpdateForm
    model = StorePageBanners
    template_name = 'management/shop/Store_banner_edit.html'
    success_url = reverse_lazy('manage_store_banners')

class StoreBannerDeleteView(StaffuserRequiredMixin,DeleteView):
    model = StorePageBanners
    template_name = 'management/shop/Store_banner_delete.html'
    success_url = reverse_lazy('manage_store_banners')


class StoreRecommendListView(StaffuserRequiredMixin,ListView):
    template_name = 'management/shop/Store_recommend_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 10
    model =  StorePageRecommend
    context_object_name = 'banners'
    def get_queryset(self):
        return StorePageRecommend.objects.all()


class StoreRecommendCreateView(StaffuserRequiredMixin,CreateView):
    form_class  = StoreRecommendCreateForm
    model = StorePageRecommend
    template_name = 'management/shop/Store_recommend_create.html'
    success_url = reverse_lazy('manage_store_recommends')

class StoreRecommendUpdateView(StaffuserRequiredMixin,UpdateView):
    form_class = StoreRecommendUpdateForm
    model = StorePageRecommend
    template_name = 'management/shop/Store_recommend_edit.html'
    success_url = reverse_lazy('manage_store_recommends')

class StoreRecommendDeleteView(StaffuserRequiredMixin,DeleteView):
    model = StorePageRecommend
    template_name = 'management/shop/Store_recommend_delete.html'
    success_url = reverse_lazy('manage_store_recommends')

class StoreIndexView(ListView):
    pass