from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField

from .models import Project, Comment, Contributor, Issue


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['role', 'project', 'contributor']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'description', 'type']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return value


class ProjectDetailSerializer(ModelSerializer):

    contributor = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user']

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise ValidationError({'title error': 'Ce titre de project existe déjà'})
        return value