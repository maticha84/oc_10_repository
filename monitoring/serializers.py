from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField

from .models import Project, Comment, Contributor, Issue


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author']

    def save(self, request):
        project = Project(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            type=self.validated_data['type'],
            author=request.user
        )
        project.save()
        return project


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['role']
