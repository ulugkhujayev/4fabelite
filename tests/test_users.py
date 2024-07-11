import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User


@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse("user-list")
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert User.objects.get().email == "test@example.com"

    def test_create_user_weak_password(self):
        url = reverse("user-list")
        data = {"email": "test@example.com", "username": "testuser", "password": "weak"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_list(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="TestPassword123!"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_user_detail(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="TestPassword123!"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "test@example.com"

    def test_update_user(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="TestPassword123!"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        data = {"username": "newusername"}
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "newusername"

    def test_delete_user(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="TestPassword123!"
        )
        self.client.force_authenticate(user=user)
        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 0
