import pytest
from django.db import IntegrityError
from django.db import transaction
from django.db.models import ProtectedError

from owmp.departments.tests.factories import DepartmentFactory
from owmp.departments.tests.factories import DepartmentMembershipFactory
from owmp.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_department_name_is_unique_ignoring_case():
    DepartmentFactory(name="Engineering")
    with pytest.raises(IntegrityError), transaction.atomic():
        DepartmentFactory(name="engineering")


def test_department_is_active_by_default():
    assert DepartmentFactory().is_active is True


def test_department_records_creation_and_update_times():
    department = DepartmentFactory()
    created = department.created_at
    department.description = "Updated"
    department.save()
    department.refresh_from_db()
    assert department.created_at == created
    assert department.updated_at >= created


def test_user_can_belong_to_several_departments():
    user = UserFactory()
    departments = DepartmentFactory.create_batch(3)
    for department in departments:
        DepartmentMembershipFactory(user=user, department=department)
    assert user.department_memberships.count() == len(departments)


def test_user_cannot_join_the_same_department_twice():
    membership = DepartmentMembershipFactory()
    with pytest.raises(IntegrityError), transaction.atomic():
        DepartmentMembershipFactory(
            user=membership.user,
            department=membership.department,
        )


def test_deactivating_a_department_keeps_its_memberships():
    membership = DepartmentMembershipFactory()
    department = membership.department
    department.is_active = False
    department.save()
    assert department.memberships.count() == 1


def test_department_with_memberships_cannot_be_deleted():
    membership = DepartmentMembershipFactory()
    with pytest.raises(ProtectedError):
        membership.department.delete()
