# accounts/models.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.utils import timezone
from django.conf import settings
from typing import Optional, List, Any


class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """

    id: int = models.AutoField(primary_key=True)
    created_at: timezone = models.DateTimeField(auto_now_add=True)
    updated_at: timezone = models.DateTimeField(auto_now=True)
    created_by: Optional[models.ForeignKey] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created",
    )

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model, providing methods to create users and superusers.
    """

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "User":
        """
        Create and return a User with an email and password.

        Parameters:
        - email (str): The email address of the user.
        - password (Optional[str]): The password for the user.
        - extra_fields (Any): Additional fields for the user.

        Returns:
        - User: The created user instance.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "User":
        """
        Create and return a superuser with an email and password.

        Parameters:
        - email (str): The email address of the superuser.
        - password (Optional[str]): The password for the superuser.
        - extra_fields (Any): Additional fields for the superuser.

        Returns:
        - User: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model that uses email as the username field.
    Includes fields for first name, last name, and role.
    """

    email: str = models.EmailField(unique=True)
    first_name: str = models.CharField(max_length=30, blank=True)
    last_name: str = models.CharField(max_length=30, blank=True)
    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)
    role: Optional[models.ForeignKey] = models.ForeignKey(
        "Role", on_delete=models.SET_NULL, null=True, blank=True
    )

    groups: models.ManyToManyField = models.ManyToManyField(
        Group,
        related_name="custom_user_set", 
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
        related_query_name="user",
    )
    user_permissions: models.ManyToManyField = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set", 
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
        related_query_name="user",
    )

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: List[str] = []

    objects: CustomUserManager = CustomUserManager()

    def __str__(self) -> str:
        """Return the string representation of the User."""
        return self.email


class Role(BaseModel):
    """
    Model representing a user role.

    Each role has a unique name and an optional description.
    """

    name: str = models.CharField(max_length=30, unique=True)
    description: str = models.TextField(blank=True)

    def __str__(self) -> str:
        """Return the string representation of the Role."""
        return self.name


class Profile(BaseModel):
    """
    Model representing a user's profile.

    Each profile is linked to a User and contains additional information
    such as date of birth, profile picture, and contact number.
    """

    user: User = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    date_of_birth: Optional[models.DateField] = models.DateField(null=True, blank=True)
    profile_picture: Optional[models.ImageField] = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    contact_number: str = models.CharField(max_length=15, blank=True)

    def __str__(self) -> str:
        """Return the string representation of the Profile."""
        return f"{self.user.email}'s profile"
