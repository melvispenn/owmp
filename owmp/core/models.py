from django.db.models import DateTimeField
from django.db.models import Model
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    """Abstract base for OWMP models: records creation and last-change times."""

    created_at = DateTimeField(_("created at"), auto_now_add=True)
    updated_at = DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True
