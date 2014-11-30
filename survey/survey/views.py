from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
# from django.core import urlresolvers
from django.contrib import messages
import datetime
import settings
from django.contrib.formtools.wizard.views import SessionWizardView

from models import Question, Survey, Category
from forms import ResponseForm
from django.contrib.formtools.wizard.forms import ManagementForm
from django import forms
from django.forms import formsets, ValidationError
from django.utils.translation import ugettext as _
from django.utils.log import getLogger

log = getLogger('dev')


def Index(request):
    return render(request, 'index.html')

def SurveyDetail(request, id):
    survey = Survey.objects.get(id=id)
    category_items = Category.objects.filter(survey=survey)

    categories = [c.name for c in category_items]
    # print 'categories for this survey:'
    # print categories
    log.info(survey)

    if request.method == 'POST':
        form = ResponseForm(request.POST, survey=survey)
        if form.is_valid():
            response = form.save()
            # return HttpResponseRedirect("/confirm/%s" % response.user_uuid)
            return HttpResponseRedirect(reverse('confirmation', args=[response.user_uuid]))
    else:
        form = ResponseForm(survey=survey)
        print form
        # TODO sort by category
    return render(request, 'survey.html', {'response_form': form, 'survey': survey, 'categories': categories})

def Confirm(request, uuid):
    email = settings.support_email
    return render(request, 'confirm.html', {'uuid':uuid, "email": email})

def privacy(request):
    return render(request, 'privacy.html')



SURVEY_TEMPLATES = [
    "survey/profile.html",
    # 'profile': 'survey/profile.html',
    "survey/life.html",
    "survey/consume.html",
    "survey/production.html",
    # ''
]

class SurveyWizard(SessionWizardView):


    def get_form_kwargs(self, step=None):
        self.survey = Survey.objects.get(pk=2)
        # log.info(self.survey)
        category_items = Category.objects.filter(survey=self.survey)
        categories = [c.id for c in category_items]
        # cid = int(step) + 1
        # categories = [c.name for c in category_items]
        try:
            cid = categories[int(step)]
        except IndexError:
            cid = 0
        return {
            'survey':self.survey,
            'cid': cid,
        }


    def get_template_names(self):
        # log.info("template %s" % self.steps.current)
        step = int(self.steps.current)
        # log.info("template %s" % SURVEY_TEMPLATES[step])
        return [SURVEY_TEMPLATES[step]]


    def render(self, form=None, **kwargs):

        category_items = Category.objects.filter(survey=self.survey)
        categories = [c.name for c in category_items]
        form = form or self.get_form()

        context = self.get_context_data(form=form,  category = categories[int(self.steps.current)], **kwargs)
        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        # return render_to_response('done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })
        # log.info(form_list)
        form = form_list[3]
        response = form.save()
        # for form in form_list:
        #     response = form.save()
        for index, form in enumerate(form_list):
            # log.info(index)
            if index == 3:
                continue
            form.save(response)
                # response = form.save()

        return HttpResponseRedirect(reverse('confirmation', args=[response.user_uuid]))