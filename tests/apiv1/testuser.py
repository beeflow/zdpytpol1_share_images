from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
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
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            get_user_model().objects.get(username=profile.get("username")).username, profile.get("username")
        )
