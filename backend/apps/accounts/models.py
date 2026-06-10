from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models import TimeStampedModel
from .managers import UserManager


class Role(models.Model):
    """System role: ADMIN, ANALYST, MANAGER, EMPLOYEE."""

    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom email-based platform user."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    STATUS_CHOICES = [(ACTIVE, "Active"), (INACTIVE, "Inactive")]

    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    department = models.CharField(max_length=255, blank=True, default="")
    position = models.CharField(max_length=255, blank=True, default="")

    roles = models.ManyToManyField(Role, related_name="users", through="UserRole")

    # Django admin/auth flags.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def role_names(self):
        return list(self.roles.values_list("name", flat=True))

    def has_role(self, name):
        return name in self.role_names


class UserRole(models.Model):
    """Explicit M2M join so the schema matches the spec's user_roles table."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_roles"
        unique_together = ("user", "role")
