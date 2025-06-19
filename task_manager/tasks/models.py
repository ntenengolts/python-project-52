from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status


User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание', blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Исполнитель'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField('labels.Label', blank=True, related_name='tasks')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
