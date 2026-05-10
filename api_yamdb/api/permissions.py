from rest_framework import permissions

# ЗАМЕТКА ДЛЯ РАЗРАБОТЧИКА №1 (Auth/User):
# Добавь эти свойства в свою модель User.
# Это позволит нам не писать везде "user.role == 'admin'",
# а использовать лаконичное "user.is_admin".
# class User(AbstractUser):
#     # ... твои поля (bio, role и т.д.) ...
#     @property
#     def is_admin(self):
#         return self.role == 'admin' or self.is_superuser or self.is_staff
#     @property
#     def is_moderator(self):
#         return self.role == 'moderator'


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