from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.web.views.note',
    url('^(?P<note_id>\d+)/poke/$', 'poke', name='web_note_poke'),
)
