from django.urls import path, include
from rest_framework.routers import DefaultRouter
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

router = DefaultRouter()
router.register(r"customer", CustomerRegistrationView)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("customer/", CustomerRegistrationView.as_view(), name="customer"),
    # path("users/", UserViewSet.as_view({"get": "list"}), name="users"),
]
