from rest_framework.permissions import BasePermission


class IsOwnerProject(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)
    """
    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False
        if obj.author != request.user:
            return False
        return request.user == obj
    """