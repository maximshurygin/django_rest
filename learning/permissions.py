from rest_framework import permissions

from users.models import UserRoles


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return obj.owner == request.user


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return not request.user.role == UserRoles.MODERATOR
        return True


class CustomViewSetPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            return not request.user.role == UserRoles.MODERATOR
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return obj.owner == request.user or request.user.role == UserRoles.MODERATOR
        return True
