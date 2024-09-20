from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, UserListView, PermissionViewSet

router = DefaultRouter()
router.register(r"permissions", PermissionViewSet, basename="permissions")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("", include(router.urls)),
]
