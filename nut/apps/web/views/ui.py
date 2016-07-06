from django.views.generic import TemplateView

class UIView(TemplateView):
    template_name = 'web/ui/ui_base.html'
