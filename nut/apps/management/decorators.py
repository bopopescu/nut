from django.http import Http404


def staff_only(func=None):
    def staff_wrapped(request, *args, **kwargs):
        if not request.user.is_staff or not request.user.editor:
            raise Http404
        return func(request, *args, **kwargs)
    return staff_wrapped


def admin_only(func=None):
    def admin_wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return func(request, *args, **kwargs)
    return admin_wrapped


def writers_only(func=None):
    def writers_wrapped(request, *args, **kwargs):
        if not request.user.can_write:
            raise Http404
        return func(request, *args, **kwargs)
    return writers_wrapped

__author__ = 'edison'
