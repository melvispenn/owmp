from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import CheckConstraint
from django.db.models import EmailField
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from utils.enums import Classification

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for OWMP.
    Account provisioning and future organization-specific fields should be
    defined only after the OWMP authentication and authorization requirements
    are approved.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    # NULL is deliberate: the initial Admin has no classification.
    classification = CharField(  # noqa: DJ001
        _("classification"),
        max_length=16,
        choices=Classification.choices,
        null=True,
        blank=True,
        default=None,
    )
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta(AbstractUser.Meta):
        constraints = [
            CheckConstraint(
                condition=Q(classification__isnull=True)
                | Q(classification__in=Classification.values),
                name="users_user_classification_valid",
            ),
        ]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
