from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
import settings
from django.contrib.formtools.wizard.views import SessionWizardView

from models import Question, Survey, Category
from forms import ResponseForm

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
            return HttpResponseRedirect("/confirm/%s" % response.user_uuid)
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




