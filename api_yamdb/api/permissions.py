from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.user.is_authenticated
                and request.user.is_moderator
                and request.method == 'DELETE'):
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.role == 'admin')


class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
