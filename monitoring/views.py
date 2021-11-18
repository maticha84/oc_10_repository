from django.shortcuts import render
from django.db.models import Value, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from monitoring.models import Project, Comment, Contributor, Issue
from authentication.models import User
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsAuthenticated


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.all()
        contributor = Contributor.objects.filter(project__in=projects, contributor=user)
        projects = Project.objects.filter(
            Q(project_contributor__in=contributor) |
            Q(author=user)
        )

        return projects

    def create(self, request):
        data = request.data
        serializer = ProjectSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)





