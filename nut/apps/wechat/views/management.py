from django.views.generic import CreateView,ListView,DeleteView
from apps.wechat.forms.management import BaseKeywordForm
from apps.wechat.models import RobotDic
from apps.core.extend.paginator import ExtentPaginator
from django.core.urlresolvers import reverse_lazy


class KeywordListView(ListView):
    template_name = 'management/wechat/management_list.html'
    paginator_class = ExtentPaginator
    paginate_by = 20
    context_object_name = 'keyword_list'
    def get_queryset(self):
        return RobotDic.objects.all().order_by('-created_datetime')


class KeywordCreateView(CreateView):
    form_class = BaseKeywordForm
    model = RobotDic
    template_name = 'management/wechat/management_create.html'
    success_url = reverse_lazy('management_wechat_keyword_list')


class KeywordDeleteView(DeleteView):
    model = RobotDic
    template_name = 'management/wechat/management_delete.html'
    success_url = reverse_lazy('management_wechat_keyword_list')
