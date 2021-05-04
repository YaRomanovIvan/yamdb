import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Overwritten class of User.

    The logic of it:
    - "email" used for registration, the filed is required
    - "username" must be unique but must be empty after registration, null=True
    """

    username_validator = UnicodeUsernameValidator()

    class UserRoles(models.TextChoices):
        ADMIN = "admin"
        USER = "user"
        MODERATOR = "moderator"

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer.Letters, digits "
            "and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
    )

    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name="Роль пользователя",
    )
    bio = models.CharField(
        max_length=50, verbose_name="Фамилия", blank=True, null=True
    )
    email = models.EmailField(
        _("email address"),
        max_length=50,
        unique=True,
        blank=False,
        db_index=True,
    )
    confirmation_code = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ["email"]

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.is_admin or self.role == self.UserRoles.MODERATOR

    USERNAME_FIELD = (
        "email"  # it's the only one field that unique and required
    )
    REQUIRED_FIELDS = [
        "username"  # it's required for users created by console
    ]
