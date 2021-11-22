from django.shortcuts import render
from django.db.models import Value, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.views import APIView

from monitoring.models import Project, Comment, Contributor, Issue
from .serializers import ProjectDetailSerializer, ProjectSerializer, ContributorSerializer
from .permissions import IsAuthenticated


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectDetailSerializer
    # detail_serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        GET method
        return : all projects concerned by the login user (contributor or autor)
        """
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(
            Q(contributor_project__in=contributor) |
            Q(contributor=user)
        )

        return projects

    def create(self, request, *args, **kwargs):
        """
        POST method
        Creation of a project with it first contributor (autor=user)

        return:
        - the created project data with code status 201 if OK
        - the serializer project errors with a status code 400 if not
        """
        project_data = request.data
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

            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        user = request.user
        project = Project.objects.get(pk=kwargs['pk'])
        contributor = Contributor.objects.filter(project=project, user=user, role='AUTHOR')

        if not contributor:
            return Response(
                {'Auteur': "Vous ne pouvez pas actualiser un projet dont vous n'êtes pas l'auteur."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        else:
            project_data = request.data
            serializer = ProjectDetailSerializer(data=project_data, partial=True)

            if serializer.is_valid():
                project = Project.objects.get(pk=kwargs['pk'])

                if 'title' in project_data:
                    project.title = project_data['title']
                if 'description' in project_data:
                    project.description = project_data['description']
                if 'type' in project_data:
                    project.type = project_data['type']

                project.save()
                serializer = ProjectDetailSerializer(project)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        project = Project.objects.get(pk=kwargs['pk'])
        contributor = Contributor.objects.filter(project=project, user=user, role='AUTHOR')

        if not contributor:
            return Response(
                {'Auteur': "Vous ne pouvez pas supprimer un projet dont vous n'êtes pas l'auteur."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        else:
            project.delete()
            return Response(
                {'Suppression': f'Suppression du projet {kwargs["pk"]} effectuée avec succès'},
                status=status.HTTP_204_NO_CONTENT
            )


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Return a list of all users.
        """
        user = self.request.user
        project_id = self.kwargs['project_id']

        projects = Project.objects.filter(id=project_id)

        contributor = Contributor.objects.filter(project__in=projects, user=user)

        if not contributor:
            data = {
                'role': "Vous n'êtes pas autorisé à effectuer cette action",
                    }
            serializer = ContributorSerializer(data, partial=True)

            return [serializer.data]

        else:
            contributors = Contributor.objects.filter(project_id=self.kwargs['project_id'])
            return contributors
