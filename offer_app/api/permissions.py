from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsBusinessUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and view.action == 'list':
            return True
        elif request.method in permissions.SAFE_METHODS and view.action == 'retrieve':
           return request.user.is_authenticated
        elif request.method in ['POST','PUT', 'PATCH', 'DELETE']:
            authenticated_business_user = bool(request.user.is_authenticated and request.user.userprofile.type == "business")
            return authenticated_business_user
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.user and request.user.is_authenticated)
            return is_owner
        return request.user.is_authenticated