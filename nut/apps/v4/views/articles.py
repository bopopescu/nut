from apps.core.views import BaseJsonView


class ArticlesListView(BaseJsonView):

    def get_data(self, context):

        return context


__author__ = 'xiejiaxin'
