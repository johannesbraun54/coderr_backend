from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response


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
            is_business_user = bool(
                request.user.userprofile.type == "business")
            return is_business_user


class ReviewPatchPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_customer_user = bool(request.user.userprofile.type == "customer")
        if request.method in permissions.SAFE_METHODS:
            return True

        elif is_customer_user and request.method in ['UPDATE','PATCH', 'DELETE']:
            is_owner = bool(request.user == obj.reviewer)
            return is_owner


class ReviewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['POST']:
            is_customer_user = bool(request.user.userprofile.type == "customer")
            return is_customer_user
