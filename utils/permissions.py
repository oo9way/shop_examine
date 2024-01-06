from rest_framework.permissions import BasePermission


class AdminsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class HasAccessShop(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        if request.user in obj.shop_admins.all():
            return True

        if request.user.is_admin:
            return True

        return False


class HasAccessProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.shop.owner == request.user:
            return True

        if request.user in obj.shop.shop_admins.all():
            return True

        if request.user.is_admin:
            return True

        return False


class IsActiveShop(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user and obj.is_active == True:
            return True

        if request.user in obj.shop.shop_admins.all() and obj.is_active == True:
            return True

        if request.user.is_admin:
            return True

        return False
