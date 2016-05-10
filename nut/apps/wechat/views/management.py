from django.views.generic import CreateView,ListView,DeleteView
from apps.wechat.forms.management import BaseKeywordForm


class KeywordListView(ListView):
    template_name = 'management/wechat/management_list.html'
    pass

class KeywordCreateView(CreateView):
    template_name = 'management/wechat/management_create.html'

    pass

class KeywordDeleteView(DeleteView):
    template_name = 'management/wechat/management_delete'
    pass