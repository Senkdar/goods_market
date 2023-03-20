from rest_framework import permissions


class AuthorOrAdminPermission(permissions.BasePermission):
    """Ограничение на просмотр объектов,
    если пользователь не является автором,
    а также на обновление контента.
    """
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_staff
        return (
            obj.user == request.user or
            request.user.is_staff
        )
