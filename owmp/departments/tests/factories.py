from factory import Sequence
from factory import SubFactory
from factory.django import DjangoModelFactory

from owmp.departments.models import Department
from owmp.departments.models import DepartmentMembership
from owmp.users.tests.factories import UserFactory


class DepartmentFactory(DjangoModelFactory[Department]):
    name = Sequence(lambda n: f"Department {n}")

    class Meta:
        model = Department


class DepartmentMembershipFactory(DjangoModelFactory[DepartmentMembership]):
    user = SubFactory(UserFactory)
    department = SubFactory(DepartmentFactory)

    class Meta:
        model = DepartmentMembership
