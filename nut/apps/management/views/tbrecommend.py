from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import requests


class RecommendView(TemplateView):
    template_name = 'management/tbrecommend/list.html'

    def get_context_data(self, **kwargs):

        context = super(RecommendView, self).get_context_data(**kwargs)
        payload = {
            'keyword':self.keyword,
            'mall':self.mall,
        }
        r = requests.get("http://10.0.2.115:10050/recommend", params=payload)
        data = r.json()
        context.update(
            {
                'object_list': data['result'],
                'keyword': self.keyword,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        self.keyword = request.GET.get('keyword', None)
        self.mall = request.GET.get('mall', False)
        assert self.keyword is not None

        return super(RecommendView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RecommendView, self).dispatch(request, *args, **kwargs)