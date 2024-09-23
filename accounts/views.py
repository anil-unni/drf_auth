from typing import Any, List
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .models import Profile, Role
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProfileSerializer,
    RoleSerializer,
)
from .utils import success_response, error_response

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing users.
    Provides actions to list, create, retrieve, update, and delete users.
    """

    queryset: List[User] = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request: Any) -> Response:
        """
        Register a new user and return JWT tokens.

        Parameters:
        - request: The request object containing user registration data.

        Returns:
        - Response: A response containing JWT tokens and user data if registration is successful,
                    or an error message if registration fails.
        """
        serializer: RegisterSerializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user: User = serializer.save()
            refresh: RefreshToken = RefreshToken.for_user(user)
            return success_response(
                data={
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": UserSerializer(user).data,
                },
                message="User registered successfully.",
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(message="Registration failed.", errors=serializer.errors)

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request: Any) -> Response:
        """
        Retrieve the authenticated user's profile.

        Parameters:
        - request: The request object of the authenticated user.

        Returns:
        - Response: A response containing the user's profile data.
        """
        serializer: UserSerializer = self.get_serializer(request.user)
        return success_response(data=serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing user profiles.
    Provides actions to list, create, retrieve, update, and delete profiles.
    """

    queryset: List[Profile] = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> List[Profile]:
        """
        Filter and return profiles related to the authenticated user.

        Returns:
        - List[Profile]: A list of profiles associated with the current user.
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer: ProfileSerializer) -> None:
        """
        Save the profile with the authenticated user as the owner.

        Parameters:
        - serializer: The serializer instance that validates and saves the profile data.
        """
        serializer.save(user=self.request.user)


class RoleViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing roles.
    Provides actions to list, create, retrieve, update, and delete roles.
    """

    queryset: List[Role] = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer: RoleSerializer) -> None:
        """
        Create and save a new role.

        Parameters:
        - serializer: The serializer instance that validates and saves the role data.
        """
        serializer.save()

class LoginView(TokenObtainPairView):
    """
    View for user login. Returns access and refresh tokens along with user data.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Call the parent post method to get tokens
        response = super().post(request, *args, **kwargs)
        
        # Get the user from the request data
        user = self.get_user(request.data['email'])
        if user:
            user_data = UserSerializer(user).data
            # Add user data to the response
            response.data.update({"user": user_data})

        return response

    def get_user(self, email: str):
        """
        Retrieve user by email.

        Parameters:
        - email (str): The email of the user.

        Returns:
        - User: The user instance or None if not found.
        """
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class LogoutView(APIView):
    """
    View for logging out a user. Blacklists the refresh token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the token if you are using token blacklisting
            RefreshToken(request.data["refresh"]).blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    """
    View for refreshing JWT tokens.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Obtain new access token
            token = RefreshToken(refresh)
            return Response(
                {
                    "access": str(token.access_token),
                    "refresh": str(token),
                }
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
