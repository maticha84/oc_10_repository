from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField

from .models import Project, Comment, Contributor, Issue


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'author_user', 'issue', 'created_time']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'project', 'tag', 'priority',
                  'status', 'author_user', 'assignee_user', 'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['role', 'project', 'user']


class ProjectDetailSerializer(ModelSerializer):
    contributor_project = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributor_project']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return value


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributor']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return value
