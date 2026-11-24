from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.db import IntegrityError
from django.db import transaction

from owmp.users.tests.factories import UserFactory
from utils.enums import Classification

if TYPE_CHECKING:
    from owmp.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.pk}/"


def test_classification_defaults_to_none():
    assert UserFactory().classification is None


@pytest.mark.parametrize("value", Classification.values)
def test_valid_classifications_are_accepted(value):
    assert UserFactory(classification=value).classification == value


def test_invalid_classification_is_rejected_by_database():
    with pytest.raises(IntegrityError), transaction.atomic():
        UserFactory(classification="CONTRACTOR")


def test_promotion_keeps_the_same_account():
    user = UserFactory(classification=Classification.INTERN)
    pk = user.pk
    user.classification = Classification.EMPLOYEE
    user.save()
    user.refresh_from_db()
    assert user.pk == pk
    assert user.classification == Classification.EMPLOYEE
