from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from monitoring.models import Contributor, Project, Issue


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        """
        Acces only for authenticated users
        """
        return bool(request.user and request.user.is_authenticated)


class IsContributor(BasePermission):
    """
    Access only for project's contributor
    """
    message = "Vous n'êtes pas contributeur du projet. Vous n'avez pas l'autorisation d'y accéder."

    def has_permission(self, request, view):

        user = request.user
        project_id = view.kwargs['project_id']

        contributor = Contributor.objects.filter(project=project_id, user=user.id)

        if not contributor:
            return False
        else:
            return True


class IsExistingProject(BasePermission):
    """
    Access only for existing projects
    """
    message = "Ce projet n'existe pas. Vous ne pouvez pas y accéder"

    def has_permission(self, request, view):

        project_id = view.kwargs['project_id']

        project = Project.objects.filter(id=project_id)

        if not project:
            raise ValidationError({"details": self.message})
        return True


class IsExistingIssue(BasePermission):
    """
    Access only for existing issues
    """
    message = "Ce problème n'existe pas. Vous ne pouvez pas y accéder"

    def has_permission(self, request, view):

        issue_id = view.kwargs['issue_id']

        issue = Issue.objects.filter(id=issue_id)

        if not issue:
            raise ValidationError({"details": self.message})
        return True
