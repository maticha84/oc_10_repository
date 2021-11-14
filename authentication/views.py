from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserSerializer, RegistrationSerializer


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class RegistrationViewset(ModelViewSet):
    serializer_class = RegistrationSerializer

    @api_view(['POST', ])
    def registration_view(self, request):
        if request.method == 'POST':
            serializer = RegistrationSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = "Enregistrement du nouvel utilisateur effectuée avec succès."
                data['email'] = user.email
                data['first_name'] = user.first_name
                data['last_name'] = user.last_name
            else:
                data = serializer.errors
            return Response(data)
