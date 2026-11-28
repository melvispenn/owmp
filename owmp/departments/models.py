from django.conf import settings
from django.db.models import CASCADE
from django.db.models import PROTECT
from django.db.models import SET_NULL
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import TextField
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from owmp.core.models import BaseModel


class Department(BaseModel):
    """An internal unit of the company. Deactivate it instead of deleting it."""

    name = CharField(_("name"), max_length=150)
    description = TextField(_("description"), blank=True)
    is_active = BooleanField(_("active"), default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="departments_department_name_ci_unique",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class DepartmentMembership(Model):
    """Links a user to a department. Membership grants no management authority."""

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="department_memberships",
    )
    department = ForeignKey(
        Department,
        on_delete=PROTECT,
        related_name="memberships",
    )
    assigned_by = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="assigned_department_memberships",
    )
    joined_at = DateTimeField(default=timezone.now)
    is_active = BooleanField(_("active"), default=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user", "department"],
                name="departments_membership_unique_user_department",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} in {self.department}"
