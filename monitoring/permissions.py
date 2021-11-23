from rest_framework.permissions import BasePermission

from monitoring.models import Contributor, Project


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        project_id = view.kwargs['project_id']
        contributor = Contributor.objects.filter(project=project_id, user=user.id)

        if not contributor:
            return False
        else:
            return True



