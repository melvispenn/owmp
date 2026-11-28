from django.contrib import admin

from .models import Department
from .models import DepartmentMembership


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(DepartmentMembership)
class DepartmentMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "is_active", "joined_at"]
    list_filter = ["is_active", "department"]
    search_fields = ["user__email", "department__name"]
