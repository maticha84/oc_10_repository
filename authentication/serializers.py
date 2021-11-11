from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError, CharField
from django.contrib.auth import password_validation

from .models import User


class UserSerializer(ModelSerializer):
    password = CharField(max_length=128, write_only=True, required=True, style={'input_type': 'password'})
    #confirm_password = CharField(max_length=128, write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', ]#'confirm_password']

    def validate_email(self, email):
        existing = User.objects.filter(email=email)
        if existing:
            raise ValidationError("Cet e-mail est déjà enregistré.")
        return email

    def validate_password(self, password):
        password_validation.validate_password(password, self.instance)
        return password

    """
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Les mots de passe ne sont pas identiques")
        return data
    """