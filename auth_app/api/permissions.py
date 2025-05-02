from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.user)
            return is_owner
        return request.user.is_authenticated

class IsStaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
