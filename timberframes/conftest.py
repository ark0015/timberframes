import pytest
from django.conf import settings

from timberframes.users.models import User
from timberframes.users.tests.factories import UserFactory


@pytest.fixture
def pytest_configure():
    settings.configure()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()
