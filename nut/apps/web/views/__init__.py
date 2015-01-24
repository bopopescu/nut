from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "web/about.html"

class Agreement(TemplateView):
    template_name = "web/agreement.html"

class JobsView(TemplateView):
    template_name = "web/jobs.html"

class FaqView(TemplateView):
    template_name = "web/base_faq.html"

class LinksView(TemplateView):
    template_name = "web/links.html"


class DownloadView(TemplateView):
    template_name = "web/download.html"
# def download_ios(request, template="download_ios.html"):
#     if request.user.is_authenticated():
#         _request_user_context = User(request.user.id).read()
#     else:
#         _request_user_context = None
#
#     return render_to_response(
#         template,
#         {
#             'user_context' : _request_user_context,
#         },
#         context_instance = RequestContext(request)
#     )


__author__ = 'edison7500'
