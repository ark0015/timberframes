import pytest
from django.test import TestCase

from timberframes.users.models import User

pytestmark = pytest.mark.django_db


class WoodTypeTests(TestCase):
    def setUp(self):
        self.user = User(name="testuser")

    def test_user_get_absolute_url(self):
        assert self.user.get_absolute_url() == f"/users/{self.user.username}/"
