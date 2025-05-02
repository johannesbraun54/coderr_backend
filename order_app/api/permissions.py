from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class EditOrderPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH']:
            is_owner = bool(obj.business_user == request.user)
            is_authenticated_business_user = bool(request.user.is_authenticated and request.user.userprofile.type == "business")
            return is_authenticated_business_user and is_owner
        
        elif request.method in ['DELETE']:
            is_staff = bool(request.user.is_staff)
            return is_staff