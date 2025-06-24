from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTests(TestCase):

    def test_create_user(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password1": "VerySecure123",
                "password2": "VerySecure123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")

    def test_update_user(self):
        user = User.objects.create_user(
            username="testuser", password="VerySecure123", first_name="OldName"
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("users:update", args=[user.id]),
            {
                "username": "updateduser",
                "first_name": "NewName",
                "last_name": "Updated",
                "email": "updated@example.com",
            },
        )
        self.assertRedirects(response, reverse("users:list"))

        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")
        self.assertEqual(user.first_name, "NewName")
        self.assertEqual(user.last_name, "Updated")
        self.assertEqual(user.email, "updated@example.com")

    def test_delete_user(self):
        user = User.objects.create_user(username="todelete", password="VerySecure123")
        self.client.force_login(user)
        response = self.client.post(reverse("users:delete", args=[user.id]))
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_update_another_user_forbidden(self):
        user1 = User.objects.create_user(username="user1", password="pass")
        user2 = User.objects.create_user(username="user2", password="pass")
        self.client.force_login(user1)

        response = self.client.post(
            reverse("users:update", args=[user2.id]), {"username": "hackeduser"}
        )
        self.assertEqual(response.status_code, 403)  # или 302, если редирект

    def test_delete_another_user_forbidden(self):
        user1 = User.objects.create_user(username="user1", password="pass")
        user2 = User.objects.create_user(username="user2", password="pass")
        self.client.force_login(user1)

        response = self.client.post(reverse("users:delete", args=[user2.id]))
        self.assertEqual(response.status_code, 403)  # или 302
