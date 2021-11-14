from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField
from django.contrib.auth import password_validation

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_email(self, email):
        existing = User.objects.filter(email=email)
        if existing:
            raise ValidationError("Cet e-mail est déjà enregistré.")
        return email

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return password


class RegistrationSerializer(ModelSerializer):
    confirm_password = CharField(max_length=128, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def validate_email(self, email):
        existing = User.objects.filter(email=email)
        if existing:
            raise ValidationError("Cet e-mail est déjà enregistré.")
        return email

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return password

    def save(self):

        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        email = self.validated_data['email']
        existing_email = User.objects.filter(email=email)
        if existing_email:
            raise ValidationError("Cet e-mail est déjà enregistré.")
        user.email = email
        password = self.validated_data['password']
        password = self.validate_password(password)
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise ValidationError({'password': 'Les mots de passe doivent être identiques'})
        user.set_password(password)
        user.save()
        return user
