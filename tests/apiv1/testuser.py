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


class UserListTest(TestCase):
    def setUp(self):
        self.faker = Faker()  # ustaiony globalnie bo bedziemy z niego korzystac :-)
        self.client = APIClient()
        self.user_model = get_user_model()
        self.username = self.faker.first_name()
        self.password = self.faker.password()

    def test_users_list_only_for_logged(self):
        response = self.client.get("/api/v1/users/", format="json")
        self.assertEqual(response.data.get("detail"), "Authentication credentials were not provided.")

    def test_users_list(self):
        self.user_model.objects.create_user(username=self.username, password=self.password)
        response = self.client.post(
            "/api/v1/auth/token/login", {"username": self.username, "password": self.password}, format="json"
        )
        token = response.data.get("auth_token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get("/api/v1/users/", format="json")
        self.assertEqual(response.data.get("count"), 1)

    def test_users_list_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.password}")
        response = self.client.get("/api/v1/users/", format="json")
        self.assertEqual(response.data.get("detail"), "Invalid token.")
