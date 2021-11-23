from django.shortcuts import render
from django.db.models import Value, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.views import APIView

from monitoring.models import Project, Comment, Contributor, Issue
from authentication.models import User
from .serializers import ProjectDetailSerializer, ProjectSerializer, ContributorSerializer
from .permissions import IsAuthenticated, IsContributor


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
    permission_classes = (IsAuthenticated, IsContributor,)

    def get_queryset(self):
        """
        Return a list of all contributors in the project.
        """

        contributors = Contributor.objects.filter(project_id=self.kwargs['project_id'])
        return contributors

    def create(self, request, *args, **kwargs):

        author = Contributor.objects.filter(project_id=self.kwargs['project_id'], user=request.user.id, role='AUTHOR')
        if not author:
            return Response(
                {"Auteur:": "Vous n'êtes pas 'auteur' du projet, vous ne pouvez pas ajouter de collaborateur."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        data = request.data
        user_email = data['user']

        user_object = User.objects.filter(email=user_email)
        for u in user_object:
            u_id = u.id
        if not user_object:
            return Response({'Utilisateur': f"{user_email} n'existe pas."},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        else:
            project_id = kwargs['project_id']
            role = data['role']

            contributor = Contributor.objects.filter(project=project_id, user=u_id)
            if contributor:
                return Response({'Contributor:': 'Cet utilisateur est déjà contributeur du projet.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:

                data = {
                    'project': project_id,
                    'role': role,
                    'user': u_id,
                }

                serializer = ContributorSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):

        author = Contributor.objects.filter(project_id=self.kwargs['project_id'], user=request.user.id, role='AUTHOR')
        if not author:
            return Response(
                {"Auteur:": "Vous n'êtes pas 'auteur' du projet, vous ne pouvez pas supprimer de collaborateur."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        try:
            delete_user = Contributor.objects.get(pk=kwargs['pk'])
            delete_user.delete()

            return Response(
                {
                    'Suppression': f'Suppression du collaborateur {kwargs["pk"]} du projet '
                                   f'{kwargs["project_id"]} effectuée avec succès'
                },
                status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(
                {
                    'Collaborateur': f"L'utilisateur {kwargs['pk']} du projet {kwargs['project_id']} n'existe pas."
                },
                status=status.HTTP_204_NO_CONTENT
            )
