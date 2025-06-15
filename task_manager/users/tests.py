from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class UserCRUDTests(TestCase):

    def test_create_user(self):
        response = self.client.post(reverse("users:create"), {
            "username": "newuser",
            "password1": "verysecure123",
            "password2": "verysecure123",
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_user(self):
        user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_login(user)
        response = self.client.post(reverse("users:update", args=[user.id]), {
            "username": "updateduser",
        })
        self.assertRedirects(response, reverse("users:list"))
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    def test_delete_user(self):
        user = User.objects.create_user(username="todelete", password="12345")
        self.client.force_login(user)
        response = self.client.post(reverse("users:delete", args=[user.id]))
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(id=user.id).exists())
