from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect



def staff_only(func=None):
    def staff_wrapped(request, *args, **kwargs):
        if not request.user.is_staff or not request.user.editor:
            raise Http404
        return func(request, *args, **kwargs)
    return staff_wrapped


__author__ = 'edison'
