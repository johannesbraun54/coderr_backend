from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class ReviewPatchPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
        if is_authenticated_customer and request.method in ['UPDATE', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.reviewer)
            return is_owner

class IsCustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST']:
            is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
            return is_authenticated_customer

    def has_object_permission(self, request, view, obj):
        is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
        if request.method in ['POST', 'PATCH']:
            return is_authenticated_customer
