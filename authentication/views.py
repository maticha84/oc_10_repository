from rest_framework.viewsets import ModelViewSet
from .serializers import RegistrationSerializer


class RegistrationViewset(ModelViewSet):
    serializer_class = RegistrationSerializer
    http_method_names = ['post', ]
