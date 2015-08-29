from apps.core.views import BaseJsonView
# from apps.core.models import Selection_Article
from apps.v4.models import APISeletion_Articles

class ArticlesListView(BaseJsonView):
    http_method_names = ['get']

    def get_data(self, context):
        sla = APISeletion_Articles.objects.published()[:10]

        res = []
        for row in sla:
            # print row.article
            res.append(
                row.api_article.v4_toDict()
            )

        return res


__author__ = 'xiejiaxin'
