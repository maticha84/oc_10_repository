from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(verbose_name='username', max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=False, verbose_name='Prénom')
    last_name = models.CharField(max_length=50, blank=False, verbose_name='Nom')
    email = models.EmailField(unique=True, verbose_name='E-mail')

    USERNAME_FIELDS = ('username',)

    def __str__(self):
        return self.email


