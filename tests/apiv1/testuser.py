from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient


class AuthTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.faker = Faker()

    def test_register(self):
        profile, password = self.faker.profile(), self.faker.password()
        response = self.client.post(
            "/api/v1/auth/register",
            {"username": profile.get("username"), "password": password, "email": profile.get("email")},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            get_user_model().objects.get(username=profile.get("username")).username, profile.get("username")
        )

    def test_login(self):
        profile, password = self.faker.profile(), self.faker.password()
        get_user_model().objects.create_user(username=profile.get("username"), password=password)

        response = self.client.post(
            "/api/v1/auth/token/login", {"username": profile.get("username"), "password": password}, format="json"
        )

        self.assertIsNotNone(response.data.get("auth_token"))
