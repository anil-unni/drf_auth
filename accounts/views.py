# accounts/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer, GroupSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Allows new users to register."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Public access


class LoginView(ObtainAuthToken):
    """Handles user login and returns authentication token."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.id, "username": user.username}
        )


class LogoutView(APIView):
    """Handles user logout by deleting the authentication token."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    """Lists all users - restricted to admin users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
    """Manages user permissions and roles."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
