from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskCRUDTests(TestCase):
    def setUp(self):
        # Создаём пользователей
        self.user = User.objects.create_user(
            username="user1", password="pass1234"
        )
        self.other_user = User.objects.create_user(
            username="user2", password="pass1234"
        )

        # Создаём статус
        self.status = Status.objects.create(name="Новый")

        # Авторизуем user
        self.client.login(username="user1", password="pass1234")

        # Создаём задачу
        self.task = Task.objects.create(
            name="Тестовая задача",
            description="Описание",
            status=self.status,
            author=self.user,
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая задача")

    def test_task_create(self):
        data = {
            "name": "Новая задача",
            "description": "Описание новой задачи",
            "status": self.status.pk,
        }
        response = self.client.post(reverse("tasks:create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="Новая задача").exists())

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("tasks:detail", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_update_by_author(self):
        data = {
            "name": "Обновлённая задача",
            "description": "Новое описание",
            "status": self.status.pk,
        }
        response = self.client.post(
            reverse("tasks:update", args=[self.task.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Обновлённая задача")

    def test_task_delete_by_author(self):
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.pk])
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_non_author_forbidden(self):
        self.client.logout()
        self.client.login(username="user2", password="pass1234")
        response = self.client.post(
            reverse("tasks:delete", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        urls = [
            reverse("tasks:list"),
            reverse("tasks:create"),
            reverse("tasks:update", args=[self.task.pk]),
            reverse("tasks:delete", args=[self.task.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"/login/?next={url}")
