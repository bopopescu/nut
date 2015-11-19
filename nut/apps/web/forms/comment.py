from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger

from apps.web.utils.formtools import innerStrip
from apps.core.models import Note_Comment
from apps.notifications import notify

log = getLogger('django')

class CommentForm(forms.Form):
    content = forms.CharField(
        label=_('content'),
        widget=forms.TextInput(attrs={'class': 'form-control comment-content'}),

    )


    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        self.user_cache = kwargs.pop('user', None)
        # print self.note, self.user_cache
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):

        _content = self.cleaned_data.get('content')
        _content = innerStrip(_content)
        # log.info("ok ok ok %s" % _content)
        _reply_to_comment_id = self.data.get('reply_to_comment_id')
        _reply_to_user_id = self.data.get('reply_to_user_id')
        comment = Note_Comment.objects.create(
            note = self.note,
            user = self.user_cache,
            content = _content,
        )
        log.info("user %s" % _reply_to_user_id)
        if _reply_to_comment_id and _reply_to_user_id:
            comment.replied_comment_id = _reply_to_comment_id
            comment.replied_user_id = _reply_to_user_id
            comment.save()
        # log.info(self.data.get('reply_to_comment_id'))
        # notify.send(comment.user, recipient=self.note.user, verb="replied", action_object=comment, target=self.note)
        return comment


__author__ = 'edison7500'
