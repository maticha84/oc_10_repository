from django.shortcuts import render
from django.db.models import Value, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status

from monitoring.models import Project, Comment, Contributor, Issue
from authentication.models import User
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorSerializer
from .permissions import IsAuthenticated


class ProjectListViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(
            Q(contributor_project__in=contributor) |
            Q(contributor=user)
        )

        return projects


class ProjectDetailViewset(ModelViewSet):
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(
            Q(contributor_project__in=contributor) |
            Q(contributor=user)
        )

        return projects

    def create(self, request, *args, **kwargs):
        project_data = request.data
        """
        project = Project.objects.create(
            title=project_data['title'],
            description=project_data['description'],
            type=project_data['type']
        )
        project.save()

        contributor = Contributor.objects.create(
            user=self.request.user,
            project=project,
            role='AUTHOR'
        )

        contributor.save()

        project.contributor.add(contributor.user)
        project.save()

        serializer = ProjectDetailSerializer(project)
        """
        serializer = ProjectDetailSerializer(data=project_data, partial=True)
        if serializer.is_valid():
            project = serializer.save()

            contributor = Contributor.objects.create(
                user=self.request.user,
                project=project,
                role='AUTHOR'
            )
            contributor.save()

            project.contributor.add(contributor.user)
            project.save()

            data = {
                'Success': "Enregistement du projet effectué avec succès",
            }
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
