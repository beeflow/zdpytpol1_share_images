from django.test import TestCase
from faker import Faker

from users.models import User


class UserTest(TestCase):
    def setUp(self) -> None:
        faker = Faker()

        self.user_a = User.objects.create_user(username=faker.profile().get("username"), password=faker.password())
        self.user_b = User.objects.create_user(username=faker.profile().get("username"), password=faker.password())

    def test_follow(self):
        self.user_a.follow(self.user_b)

        self.user_a.refresh_from_db()
        self.user_b.refresh_from_db()

        self.assertEqual(self.user_a.followed.count(), 1)
        self.assertEqual(self.user_a.followers.count(), 0)
        self.assertEqual(self.user_b.followers.count(), 1)
        self.assertEqual(self.user_b.followed.count(), 0)

    def test_shoud_raise_integrity_error(self):
        self.user_a.follow(self.user_b)
        self.user_a.follow(self.user_b)
