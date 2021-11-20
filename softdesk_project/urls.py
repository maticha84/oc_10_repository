"""softdesk_project URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset, RegistrationViewset
from monitoring.views import ProjectViewset


router = routers.SimpleRouter()
router.register('users', UserViewset, basename='users')
router.register('signup', RegistrationViewset, basename='signup')
router.register('projects', ProjectViewset, basename='projects')

urlpatterns = [
    path('objects/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]