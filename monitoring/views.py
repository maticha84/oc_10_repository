from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from monitoring.models import Project, Comment, Contributor, Issue
from authentication.models import User
from .serializers import ProjectDetailSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import (
    IsAuthenticated,
    IsContributor,
    IsExistingProject,
    IsExistingIssue,
    IsAuthorProject,
    IsAuthorIssue,
    IsAuthorComment)


class ProjectViewset(ModelViewSet):
    """
    class for Project Viewset
    --> get all projects concerned by the authenticated user
    --> create a new project
    --> update a project
    --> delete (destroy) a project
    """
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated, IsAuthorProject)

    def get_queryset(self):
        """
        GET method

        return : all projects concerned by the login user (contributor or author)
        """
        user = self.request.user
        projects = Project.objects.all()

        contributor = Contributor.objects.filter(project__in=projects, user=user)
        projects = Project.objects.filter(contributor_project__in=contributor)

        return projects

    def create(self, request, *args, **kwargs):
        """
        POST method
        Creation of a project with it first contributor (autor=user)

        fields : title, description, type (author auto create in a contributor object and add to the project)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        PUT method
        Modification of a project

        fields : title, description, type

        return: the saved project data with code status 202 ACCEPTED if OK,
        404 NOT FOUND if not found and 403 FORBIDDEN if user is not author
        """

        project = Project.objects.filter(pk=kwargs['pk'])
        if not project:
            return Response(
                {'Projet': f"Le projet {kwargs['pk']} n'existe pas. Vous ne pouvez pas le mettre à jour."},
                status=status.HTTP_404_NOT_FOUND
            )
        project = project.get()

        project_data = request.data
        serializer = ProjectDetailSerializer(data=project_data, partial=True)

        if serializer.is_valid():
            if 'title' in project_data:
                project.title = project_data['title']
            if 'description' in project_data:
                project.description = project_data['description']
            if 'type' in project_data:
                project.type = project_data['type']

            project.save()
            serializer = ProjectDetailSerializer(project)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        Deletion of a project

        return : 204 NO CONTENT if ok, 404 NOT FOUND if not found and 405 NOT ALLOWED if user is not author
        """
        project = Project.objects.filter(pk=kwargs['pk'])
        if not project:
            return Response(
                {'Projet': f"Le projet {kwargs['pk']} n'existe pas. Vous ne pouvez pas le supprimer."},
                status=status.HTTP_404_NOT_FOUND
            )
        project = project.get()
        project.delete()
        return Response(
            {'Suppression': f'Suppression du projet {kwargs["pk"]} effectuée avec succès'},
            status=status.HTTP_204_NO_CONTENT
        )


class ContributorViewset(ModelViewSet):
    """
        class for contributor Viewset
        --> get all contributors concerned by the project
        --> add a new contributor
        --> delete (destroy) a contributor
        """
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, IsExistingProject, IsContributor, IsAuthorProject)

    def get_queryset(self):
        """
        GET Method

        Return: list of all contributors in the project.
        """
        contributors = Contributor.objects.filter(project_id=self.kwargs['project_id'])
        return contributors

    def create(self, request, *args, **kwargs):
        """
        POST Method
        Add a new contributor to a project : may be a CONTRIBUTOR or an AUTHOR. Multi author is allowed.

        fields : user, project, role

        return :
        if not AUTHOR of the project --> 403 FORBIDDEN
        if user doesn't exist in the base --> 404 not found
        if user is already a contributor of the project --> 400 BAD REQUEST
        if errors in the data fields --> 400 BAD REQUEST
        if OK --> 201 CREATED
        """

        author = Contributor.objects.filter(project_id=self.kwargs['project_id'], user=request.user.id, role='AUTHOR')
        if not author:
            return Response(
                {"detail:": "Vous n'êtes pas auteur du projet. Vous n'avez pas l'autorisation de modifier/supprimer"},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        user_email = data['user']

        user_object = User.objects.filter(email=user_email)
        for u in user_object:
            u_id = u.id
        if not user_object:
            return Response({'Utilisateur': f"{user_email} n'existe pas."},
                            status=status.HTTP_404_NOT_FOUND
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
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        delete a contributor to a project

        return :
        if not AUTHOR of the project --> 403 FORBIDDEN
        if user doesn't exist in the base --> 404 not found
        if OK --> 204 NO CONTENT
        """
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
                status=status.HTTP_404_NOT_FOUND
            )


class IssueViewset(ModelViewSet):
    """
    class for Issue Viewset
    --> get all issue concerned by the project
    --> create a new issue
    --> update an issue
    --> delete (destroy) an issue
    """
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IsExistingProject, IsContributor,IsAuthorIssue)

    def get_queryset(self):
        """
        GET Method

        return : all issues of a project
        """
        issues = Issue.objects.filter(project_id=self.kwargs['project_id'])
        return issues

    def create(self, request, *args, **kwargs):
        """
        POST Method
        Create an issue to a project. User be atomatically the author of this created issue.

        fields : title, desc, tag, priority, status, assignee_user

        return :
        if OK --> 201 CREATED
        if title already exists --> 400 BAD REQUEST
        if assignee_user does not exist --> 404 NOT FOUND
        if data validation is not OK --> 400 BAD REQUEST
        """
        data = request.data
        project_id = kwargs['project_id']
        author_user = request.user

        issues = Issue.objects.filter(project=project_id, title=data['title'])
        if issues:
            return Response(
                {
                    "Titre": "Il existe déjà un problème avec un titre identique. Veuillez changer le titre."
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if data['assignee_user'] == '':
            assignee_user = request.user.id
        else:
            try:
                user = User.objects.get(email=data['assignee_user'])
                assignee_user = user.id

            except:
                return Response(
                    {
                        "Utilisateur assigné": f"L'utilisateur {data['assignee_user']} n'existe pas et ne peut pas "
                                               f"être assigné à ce problème."
                    }, status=status.HTTP_404_NOT_FOUND
                )
        new_issue_data = {
            'title': data['title'],
            'desc': data['desc'],
            'tag': data['tag'],
            'priority': data['priority'],
            'status': data['status'],
            'author_user': author_user.id,
            'project': project_id,
            'assignee_user': assignee_user
        }
        serializer = IssueSerializer(data=new_issue_data, partial=True)
        if serializer.is_valid(project_id):
            new_issue = serializer.save()
            serializer = IssueSerializer(new_issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        PUT Method
        Update an issue to a project.

        fields : title, desc, tag, priority, status, assignee_user

        return :
        if OK --> 202 accepted
        if issue doesn't exist --> 404 NOT FOUND
        if issue's author != user --> 403 FORBIDDEN
        if title already exists --> 400 BAD REQUEST
        if assignee_user does not exist --> 404 NOT FOUND
        if data validation is not OK --> 400 BAD REQUEST
        """
        project_id = kwargs['project_id']
        issue = Issue.objects.filter(pk=kwargs['pk'])
        if not issue:
            return Response(
                {
                    'Issue': f"Le problème {kwargs['pk']} n'existe pas. Vous ne pouvez pas le modifier."
                }, status=status.HTTP_404_NOT_FOUND
            )

        issue = issue.get()
        issue_data = request.data
        data = {}
        if 'assignee_user' in issue_data:
            user = User.objects.filter(email=issue_data['assignee_user'])
            if not user:
                return Response(
                    {
                        "Utilisateur assigné": f"L'utilisateur {issue_data['assignee_user']} "
                                               f"n'existe pas et ne peut pas "
                                               f"être assigné à ce problème."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = user.get()
            issue.assignee_user = user
            data['assignee_user'] = user.id
        if 'title' in issue_data:
            issues = Issue.objects.filter(project=project_id, title=issue_data['title'])
            if issues:
                return Response(
                    {
                        "Titre": "Il existe déjà un problème avec un titre identique. Veuillez changer le titre."
                    },
                    status.HTTP_400_BAD_REQUEST
                )
            issue.title = issue_data['title']
            data['title'] = issue_data['title']
        if 'desc' in issue_data:
            issue.desc = issue_data['desc']
            data['desc'] = issue_data['desc']
        if 'tag' in issue_data:
            issue.tag = issue_data['tag']
            data['tag'] = issue_data['tag']
        if 'priority' in issue_data:
            issue.priority = issue_data['priority']
            data['priority'] = issue_data['priority']
        if 'status' in issue_data:
            issue.status = issue_data['status']
            data['status'] = issue_data['status']

        serializer = IssueSerializer(data=data, partial=True)

        if serializer.is_valid():

            issue.save()
            serializer = IssueSerializer(issue)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        DELETE an issue to a project.

        return :
        if OK --> 204 NO CONTENT
        if issue doesn't exist --> 404 NOT FOUND
        if issue's author != user --> 403 FORBIDDEN
        if data validation is not OK --> 400 BAD REQUEST
        """
        user = request.user
        issue = Issue.objects.filter(pk=kwargs['pk'])
        if not issue:
            return Response(
                {
                    'Issue': f"Le problème {kwargs['pk']} n'existe pas. Vous ne pouvez pas le supprimer."
                }, status=status.HTTP_404_NOT_FOUND
            )

        issue = issue.get()
        issue.delete()
        return Response(
            {
                'Suppression': f'Suppression du problème {kwargs["pk"]} du projet '
                               f'{kwargs["project_id"]} effectuée avec succès'
            },
            status=status.HTTP_204_NO_CONTENT)


class CommentViewset(ModelViewSet):
    """
    class for Comment Viewset
    --> get all comment concerned by the issue
    --> get a comment using his ID
    --> create a new comment
    --> update a comment
    --> delete (destroy) an comment
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsExistingProject, IsExistingIssue, IsContributor, IsAuthorComment)

    def get_queryset(self):
        """
        GET Method

        return : all comments to an issue.
        """
        comments = Comment.objects.filter(issue_id=self.kwargs['issue_id'])
        return comments

    def create(self, request, *args, **kwargs):
        """
        POST Method
        create a new comment for an issue. author is automatically the user who create the issue,
        issue is automatically completed

        fields : description

        returns :
        if no description (in body or in data) --> 400 BAD REQUEST
        if OK --> 201 CREATED
        """
        data = request.data

        if not 'description' in data:
            return Response(
                {
                    'description': "Le couple clef / valeur 'description' doit être renseignée dans la partie 'body'"
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=data, partial=True)

        if serializer.is_valid():
            comment_data = {}
            author_user = request.user
            issue = Issue.objects.get(pk=kwargs['issue_id'])

            comment_data['author_user'] = author_user.id
            comment_data['issue'] = issue.id
            comment_data['description'] = data['description']

            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        POST Method
        create a new comment for an issue. author is automatically the user who create the issue,
        issue is automatically completed

        fields : description

        returns :
        if no description (in body or in data) --> 400 BAD REQUEST
        if comment does'nt exist --> 404 NOT FOUND
        if comment's author != user --> 403 FORBIDDEN
        if OK --> 202 ACCEPTED
        """
        data = request.data
        if not 'description' in data:
            return Response(
                {
                    'description': "Le couple clef / valeur 'description' doit être renseignée dans la partie 'body'"
                }, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.filter(pk=kwargs['pk'])
        if not comment:
            return Response(
                {
                    'Comment': f"Le commentaire avec l'id {kwargs['pk']} n'existe pas. Vous ne pouvez pas le modifier"
                }, status=status.HTTP_404_NOT_FOUND
            )

        comment = comment.get()
        serializer = CommentSerializer(data=data, partial=True)
        if serializer.is_valid():
            comment.description = data['description']
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE Method
        delete a comment

        return :
        if comment doesn't exist --> 404 NOT FOUND
        if comment's author != user --> 403 FORBIDDEN
        if OK --> 204 NO CONTENT
        """
        user = request.user

        comment = Comment.objects.filter(pk=kwargs['pk'])
        if not comment:
            return Response(
                {
                    'Comment': f"Le commentaire avec l'id {kwargs['pk']} n'existe pas. Vous ne pouvez pas le supprimer"
                }, status=status.HTTP_404_NOT_FOUND
            )
        comment = comment.get()
        comment.delete()
        return Response(
            {
                'Suppression': f'Suppression du commentaire {kwargs["pk"]} du problème '
                               f'{kwargs["issue_id"]} effectuée avec succès'
            },
            status=status.HTTP_204_NO_CONTENT)
