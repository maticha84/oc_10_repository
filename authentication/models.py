from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Prénom')
    last_name = models.CharField(max_length=30, verbose_name='Nom')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
