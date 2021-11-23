"""softdesk_project URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset, RegistrationViewset
from monitoring.views import ProjectViewset, ContributorViewset, IssueViewset


router = routers.SimpleRouter()
router.register('users', UserViewset, basename='users')
router.register('signup', RegistrationViewset, basename='signup')
router.register('projects', ProjectViewset, basename='projects')
sub_router1 = routers.SimpleRouter()
sub_router1.register('contributors', ContributorViewset, basename='contributors')
sub_router1.register('issues', IssueViewset, basename='issues')


urlpatterns = [
    path('objects/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<int:project_id>/', include(sub_router1.urls)),
]
