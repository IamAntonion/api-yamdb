from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение только для администратора."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_admin
        )


class IsAuthenticatedUser(permissions.BasePermission):
    """Разрешение только для авторизированного пользователя."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """Разришение на полное чтение и запись ограниченным лицам."""

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
    """Чтение всем, остальное для админа."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
