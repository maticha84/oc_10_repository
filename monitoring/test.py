from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from authentication.models import User
from .models import Comment, Contributor, Project, Issue


class TestUser(APITestCase):
    url = reverse_lazy('user_list')

    def test_user(self):
        User.objects.create(username='test', email='test@test.fr', password='p@ssw0rd!')
        user = User.objects.get(username='test')
        self.assertEqual(user.email, 'test@test.fr')


class TestProjects(APITestCase):
    pass
