from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField

from .models import Project, Comment, Contributor, Issue


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['role', 'project', 'user']


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type']

    def validate_title(self, title):
        if Project.objects.filter(title=title).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return title


class ProjectDetailSerializer(ModelSerializer):

    contributor_project = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'contributor_project']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return value

