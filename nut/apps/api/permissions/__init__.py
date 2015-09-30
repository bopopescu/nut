from  rest_framework import permissions


class Admin_write_only(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user and request.user.is_staff

class Admin_And_Editor_Only(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (hasattr(request.user,'is_admin') and \
               hasattr(request.user,'is_editor')) and \
               (request.user.is_admin or request.user.is_editor)
