from rest_framework.permissions import BasePermission


class AdminsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
