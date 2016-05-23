from braces.views._access import AccessMixin

class EditorRequiredMixin(AccessMixin):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_editor):
            return self.handle_no_permission(request)
        return super(EditorRequiredMixin, self).dispatch(
            request, *args, **kwargs)