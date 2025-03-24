from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS



class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.user)
            return is_owner
            
class IsBusinessUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['POST']:
            is_business_user =  bool(request.user.userprofile.type == "business")
            return is_business_user