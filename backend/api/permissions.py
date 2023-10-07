from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdminOrReadOnly(BasePermission):
    '''
    Разрешение на создание, изменение, удаление
    для автора и администратора. Чтение доступно всем.
    '''

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (obj.author == request.user
                    or request.user.role == 'admin'
                    or request.user.is_staff))
