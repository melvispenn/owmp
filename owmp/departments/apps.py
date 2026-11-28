from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DepartmentsConfig(AppConfig):
    name = "owmp.departments"
    verbose_name = _("Departments")
