from django.views.generic import TemplateView


class SelectionStatisticsView(TemplateView):
    template_name = 'management/statistics/selection.html'

