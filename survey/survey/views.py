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
from django import forms

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
    # 'life': 'survey/life.html',
    # ''
]

class SurveyWizard(SessionWizardView):

    # def get_form_initial(self, step):
    #     log.info(step)
    #     survey = Survey.objects.get(pk=1)
    #     return self.initial_dict.get(step, {'survey': survey})
    #
    # def get_form_instance(self, step):
    #     log.info(self.initial_dict)

    def get(self, request, sid, *args, **kwargs):
        self.storage.reset()
        self.storage.current_step = self.steps.first
        self.survey = Survey.objects.get(pk=sid)
        category_items = Category.objects.filter(survey=self.survey)

        categories = [c.name for c in category_items]

        return self.render(self.get_form(), survey = self.survey, category = categories[int(self.steps.current)])

    def get_form(self, step=None, data=None, files=None):
        step = self.steps.current
        kwargs = self.get_form_kwargs(step)
        # survey = Survey.objects.get(pk=1)
        cid = int(step) + 1

        # self.survey.question_set.filter(category_id=cid)
        kwargs.update({
            'data': data,
            'files': files,
            'prefix': self.get_form_prefix(step, self.form_list[step]),
            'initial': self.get_form_initial(step),
            'survey':self.survey,
            'cid': cid,
            # 'category': self.survey.question_set.filter(category=1),
        })


        if issubclass(self.form_list[step], forms.ModelForm):
            # If the form is based on ModelForm, add instance if available
            # and not previously set.
            kwargs.setdefault('instance', self.get_form_instance(step))
        elif issubclass(self.form_list[step], forms.models.BaseModelFormSet):
            # If the form is based on ModelFormSet, add queryset if available
            # and not previous set.
            kwargs.setdefault('queryset', self.get_form_instance(step))
        log.info(kwargs)
        return self.form_list[step](**kwargs)
        # return super(SurveyWizard, self).get_form(step, data, files)

    def get_template_names(self):
        # log.info(self.steps)
        return [SURVEY_TEMPLATES[0]]

    def render(self, form=None, **kwargs):
        form = form or self.get_form()

        # log.info(form)
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        # return render_to_response('done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })

        return HttpResponseRedirect(reverse('confirmation', args=[response.user_uuid]))