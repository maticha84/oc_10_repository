from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from .permissions import IsAuthenticatedAdmin


class UserViewset(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedAdmin,)

    def get_queryset(self):
        return User.objects.all()


class RegistrationViewset(ModelViewSet):
    serializer_class = RegistrationSerializer
    http_method_names = ['post', ]
