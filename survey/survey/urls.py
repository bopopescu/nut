from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()
media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'survey.views.Index', name='home'),
    url(r'^survey/$', 'survey.views.Index', name='home'),
    url(r'^survey/confirm/(?P<uuid>\w+)/$', 'survey.views.Confirm', name='confirmation'),

    # url(r'^survey/(?P<id>\d+)/$', 'survey.views.SurveyDetail', name='survey_detail'),

    url(r'^privacy/$', 'survey.views.privacy', name='privacy_statement'),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^survey/admin/', include(admin.site.urls)),
)


from survey.views import SurveyWizard
from survey.forms import ResponseWizardFrom, ResponseWithOutUsernameWizardFrom
SurveyForms = [ResponseWizardFrom,
               ResponseWithOutUsernameWizardFrom,
               ResponseWithOutUsernameWizardFrom,
               ResponseWithOutUsernameWizardFrom]

urlpatterns += patterns(
    'survey.views',
    url(r'^survey/(?P<sid>\d+)/$', SurveyWizard.as_view(SurveyForms), name='surveies'),
)

# media url hackery. le sigh. 
urlpatterns += patterns('',
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT, 'show_indexes':True }),
)

