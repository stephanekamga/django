from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegistrationView, UserProfileView, LogoutView, AccidentListView, UtilisateurViewSet

urlpatterns = [
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/accidents/', AccidentListView.as_view(), name='accident-list'),
    path('api/utilisateurs/', UtilisateurViewSet.as_view(), name='users-list'),
]
