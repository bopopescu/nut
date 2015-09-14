from apps.core.views import BaseJsonView
# from apps.core.models import Selection_Article
from apps.v4.models import APISeletion_Articles
from apps.mobile.lib.sign import check_sign

from django.core.paginator import Paginator
from datetime import datetime
import time

class ArticlesListView(BaseJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        sla_list = APISeletion_Articles.objects.\
            published_until(until_time=self.timestamp).\
            order_by('-pub_time')

        paginator = Paginator(sla_list, self.size)

        res = []
        try:
            sla = paginator.page(self.page)
        except Exception:
            return res

        for row in sla.object_list:
            a = row.api_article.v4_toDict()
            a.update(
                {
                    'pub_time': time.mktime(row.pub_time.timetuple())
                }
            )
            res.append(
                a
            )

        return res

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.size = request.GET.get('size', 10)
        self.timestamp = request.GET.get('timestamp', None)
        if self.timestamp != None:
            self.timestamp = datetime.fromtimestamp(float(self.timestamp))
        return super(ArticlesListView, self).get(request, *args, **kwargs)

    @check_sign
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlesListView, self).dispatch(request, *args, **kwargs)



__author__ = 'xiejiaxin'
