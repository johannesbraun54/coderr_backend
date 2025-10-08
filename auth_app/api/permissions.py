from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Check if the user is authenticated and is the owner of the object or has staff privileges.   
    If the user is the owner, they can perform PUT, PATCH, and DELETE operations.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.user)
            return is_owner
        return request.user.is_authenticated
    

class IsStaffPermission(permissions.BasePermission):
    """
    Check if the user has staff privileges.
    Only staff users are granted permission.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
