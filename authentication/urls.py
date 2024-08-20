from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, LogoutView, CustomerRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("customer/", CustomerRegistrationView.as_view(), name="customer"),
]
