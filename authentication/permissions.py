from rest_framework.permissions import BasePermission


class IsAuthenticatedAdmin(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
