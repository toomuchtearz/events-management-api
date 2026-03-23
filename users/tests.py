from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("users:create")
        self.me_url = reverse("users:manage")
        self.user_data = {
            "email": "test@example.com",
            "password": "Password123!",
            "first_name": "Illia",
            "last_name": "Khomutov",
        }

    def test_create_user_with_email_successful(self):
        user = User.objects.create_user(
            email="newuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.email, "newuser@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)

    def test_new_user_email_normalized(self):
        email = "TEST@EXAMPLE.COM"
        user = User.objects.create_user(
            email,
            "pass123", first_name="A", last_name="B")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(None, "pass123")

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="password123",
            first_name="Admin",
            last_name="User",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_full_name_property(self):
        """Test the full_name property logic."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.full_name, "Illia Khomutov")

    def test_create_user_api_successful(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertNotIn("password", response.data)

    def test_create_user_missing_fields(self):
        payload = {"email": "bad@test.com", "password": "Password123!"}
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_retrieve_profile_authenticated(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["first_name"], user.first_name)

    def test_retrieve_profile_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_successful(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        payload = {"first_name": "UpdatedName"}
        response = self.client.patch(self.me_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "UpdatedName")

    def test_email_is_read_only_in_manage(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        payload = {"email": "hacker@test.com"}
        response = self.client.patch(self.me_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.email, self.user_data["email"])
