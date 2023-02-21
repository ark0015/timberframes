import pytest
from django.conf import settings

from timberframes.users.models import User
from timberframes.users.tests.factories import UserFactory


def pytest_configure():
    settings.configure(DATABASES=...)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()
