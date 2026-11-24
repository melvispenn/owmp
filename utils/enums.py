from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Classification(TextChoices):
    EMPLOYEE = "EMPLOYEE", _("Employee")
    INTERN = "INTERN", _("Intern")
