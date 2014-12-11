from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger

from apps.core.models import Note_Comment

log = getLogger('django')

class CommentForm(forms.Form):
    content = forms.CharField(
        label=_('content'),
        widget=forms.TextInput(attrs={'class':'form-control comment-content'}),
        help_text=_(''),
    )


    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        self.user_cache = kwargs.pop('user', None)
        # print self.note, self.user_cache
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):

        _content = self.cleaned_data.get('content')
        log.info("ok ok ok %s" % _content)
        comment = Note_Comment.objects.create(
            note = self.note,
            user = self.user_cache,
            content = _content,
        )

        return comment


__author__ = 'edison7500'
