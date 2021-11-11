from rest_framework.permissions import BasePermission


class IsOwnerProject(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)

    def has_object_persmission(self, request, view, obj):
        return request.user == obj