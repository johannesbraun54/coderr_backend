from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response


class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.user)
            return is_owner


class IsBusinessUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST', 'PATCH']:
            authenticated_business_user = bool(request.user.is_authenticated and request.user.userprofile.type == "business")
            if authenticated_business_user:
                return True


class IsStaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class ReviewPatchPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
        if is_authenticated_customer and request.method in ['UPDATE', 'PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.reviewer)
            return is_owner


class IsCustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        elif request.method in ['POST']:
            is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
            return is_authenticated_customer

    def has_object_permission(self, request, view, obj):
        is_authenticated_customer = bool(request.user.is_authenticated and request.user.userprofile.type == "customer")
        if request.method in ['POST', 'PATCH']:
            return is_authenticated_customer


class EditOrderPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH']:
            is_business_user = bool(request.user.userprofile.type == "business")
            return is_business_user
        
        elif request.method in ['DELETE']:
            is_staff = bool(request.user.is_staff)
            return is_staff
