from  rest_framework import permissions


class Admin_And_Editor_Only(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (hasattr(request.user,'is_admin') and \
               hasattr(request.user,'is_editor')) and \
               (request.user.is_admin or request.user.is_editor)
