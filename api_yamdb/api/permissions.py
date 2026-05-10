from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_admin
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_moderator
        )


class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminUserOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
