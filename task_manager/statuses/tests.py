from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

User = get_user_model()


class StatusCRUDTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="pass"
        )
        cls.status = Status.objects.create(name="In Progress")

    def setUp(self):
        self.client.force_login(self.user)

    def test_status_list_view(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "In Progress")

    def test_create_status(self):
        response = self.client.post(reverse("statuses:create"), {"name": "New"})
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="New").exists())

    def test_update_status(self):
        response = self.client.post(
            reverse("statuses:update",
            args=[self.status.id]),
            {"name": "Updated"}
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated")

    def test_delete_status(self):
        response = self.client.post(
            reverse("statuses:delete", args=[self.status.id])
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_login_required(self):
        self.client.logout()
        protected_urls = [
            reverse("statuses:list"),
            reverse("statuses:create"),
            reverse("statuses:update", args=[self.status.id]),
            reverse("statuses:delete", args=[self.status.id]),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse("login")))
