from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    UserRegistrationView,
    LogoutView,
    CustomerRegistrationView,
    CustomTokenObtainPairView,
    UserViewSet,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("customer/", CustomerRegistrationView.as_view(), name="customer"),
    path("users/", UserViewSet.as_view({"get": "list"}), name="users"),
]
