from django.http import Http404, HttpResponseForbidden


def staff_and_editor(func=None):
    def staff_wrapped(*args, **kwargs):
        if len(args) == 2:
            request = args[1]
        else:
            request = args[0]
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if not (request.user.is_staff or request.user.is_editor):
            raise Http404
        return func(*args, **kwargs)
    return staff_wrapped


def staff_only(func=None):
    def staff_wrapped(*args, **kwargs):
        if len(args) == 2:
            request = args[1]
        else:
            request = args[0]
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if not request.user.is_staff or not request.user.editor:
            raise Http404
        return func(*args, **kwargs)
    return staff_wrapped


def admin_only(func=None):
    def admin_wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if not request.user.is_staff:
            raise Http404
        return func(request, *args, **kwargs)
    return admin_wrapped


def writers_only(func=None):
    def writers_wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        if not request.user.can_write:
            raise Http404
        return func(request, *args, **kwargs)
    return writers_wrapped
