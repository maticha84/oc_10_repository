from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField

from .models import Project, Comment, Contributor, Issue


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author']
