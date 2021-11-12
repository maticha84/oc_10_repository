from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from .models import Project, Comment, Contributor, Issue
from .serializers import ProjectSerializer
from .permissions import IsOwnerProject


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwnerProject,)

    def get_queryset(self):
        return Project.objects.all()
